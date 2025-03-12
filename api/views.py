from venv import logger
from django.shortcuts import render
from rest_framework import generics,status
from django.contrib.auth import authenticate, login,get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login



from .serializers import (
    UserSerializer,
    RecipeSerializer,
    CategorySerializer,
    TagSerializer,
    CommentSerializer,
    BlogSerializer,
    UserProfileSerializer
)
from .models import Recipes, Category, Tag, Comment,Blog,User
User = get_user_model()

logger = logging.getLogger(__name__)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'detail': 'User created successfully',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Both email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                if not user.is_staff:  # Ensure it's not an admin
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        "message": "User logged in successfully",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    }, status=status.HTTP_200_OK)
                return Response(
                    {"error": "Admin accounts cannot log in here"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except User.DoesNotExist:
            return Response(
                {"error": "No user found with this email"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {"error": "An error occurred during login"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # To handle file uploads

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            # Delete old profile picture if it exists
            if instance.profile_picture:
                instance.profile_picture.delete(save=False)
        
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial,
            context={'request': request}
        )
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class AdminLoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            if not email or not password:
                return Response(
                    {'error': 'Please provide both email and password'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Authenticate user
            user = authenticate(email=email, password=password)
            
            if not user:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Check if user is an admin
            if not user.is_admin:  # Assuming you have an is_admin field in your User model
                return Response(
                    {'error': 'Access denied. Admin privileges required.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Generate tokens for admin
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'status': 'success',
                'message': 'Admin login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'is_admin': user.is_admin
                }
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                {'error': 'User does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Fetch admin dashboard data
        total_recipes = Recipes.objects.count()
        total_users = User.objects.count()
        total_categories = Category.objects.count()
        total_tags = Tag.objects.count()

        return Response({
            'total_recipes': total_recipes,
            'total_users': total_users,
            'total_categories': total_categories,
            'total_tags': total_tags
        })

class AdminUserManagementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Fetch all users with their details
        users = User.objects.all().values('id', 'username', 'email', 'is_active', 'date_joined')
        return Response(users)
    
        

    def put(self, request, user_id):
        # Enable/disable user account
        try:
            user = User.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()
            return Response({
                'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
                'is_active': user.is_active
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Prevent email/username update if they already exist
            new_email = serializer.validated_data.get('email')
            new_username = serializer.validated_data.get('username')
            
            if new_email and new_email != user.email:
                if User.objects.filter(email=new_email).exists():
                    return Response(
                        {"error": "Email already exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if new_username and new_username != user.username:
                if User.objects.filter(username=new_username).exists():
                    return Response(
                        {"error": "Username already exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {"error": "Both old and new passwords are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify old password
        if not user.check_password(old_password):
            return Response(
                {"error": "Current password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Validate new password
            validate_password(new_password, user)
            
            # Set new password
            user.set_password(new_password)
            user.save()
            
            # Generate new tokens since password changed
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Password updated successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
            
        except ValidationError as e:
            return Response(
                {"error": list(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "An error occurred while updating password"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Recipe views
class CreateRecipeView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]
    # queryset = Recipes.objects.filter(is_public=True)
    parser_classes = (MultiPartParser, FormParser)  # Important for file uploads

    # def get_queryset(self):
    #     user = self.request.user
    #     return Recipes.objects.filter(author=user)

    def perform_create(self, serializer):
        # Check if an image was uploaded
        image = self.request.data.get('image')
        
        # Save the recipe with the author and optional image
        serializer.save(author=self.request.user, image=image)


class RecipeDelete(generics.DestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Recipes.objects.filter(author=user)


class RecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Recipes.objects.all()

class RecipeDetailView(generics.RetrieveAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Recipes.objects.filter(author=user)


class RecipeUpdateView(generics.UpdateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Recipes.objects.filter(author=user)


# Category views
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()


# Tag views
class TagListCreateView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()


# Comment views
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        recipe_id = self.kwargs.get("recipe_id")
        return Comment.objects.filter(recipe_id=recipe_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(user=user)

class SharedRecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recipes.objects.filter(is_public=True)
    
class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny] 
    queryset = Blog.objects.filter(is_public=True)
    parser_classes = (MultiPartParser, FormParser)  # Important for file uploads

    # def get_queryset(self):
    #     user = self.request.user
    #     return Blog.objects.filter(author=user)

    def perform_create(self, serializer):
        # Check if an image was uploaded
        image = self.request.data.get('image')
        
        # Save the recipe with the author and optional image
        serializer.save(author=self.request.user, image=image)


class BlogDetailView(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]  
    queryset = Blog.objects.filter(is_public=True)

class MyBlogsView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

class BlogUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

   