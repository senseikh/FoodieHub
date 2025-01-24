from venv import logger
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics,status
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from .serializers import (
    UserSerializer,
    RecipeSerializer,
    CategorySerializer,
    TagSerializer,
    CommentSerializer,
)
from .models import Recipes, Category, Tag, Comment


# User creation view
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_staff:  # Ensure it's not an admin
                login(request, user)
                return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Admin accounts cannot log in here"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extract credentials
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            logger.warning("Login attempt with missing credentials")
            return Response({
                "error": "Username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Authenticate user
            user = authenticate(request, username=username, password=password)

            # Check authentication
            if user is None:
                logger.warning(f"Failed login attempt for username: {username}")
                return Response({
                    "error": "Invalid credentials"
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Check admin status
            if not user.is_staff:
                logger.warning(f"Non-admin user {username} attempted to log in")
                return Response({
                    "error": "Access denied. Admin privileges required."
                }, status=status.HTTP_403_FORBIDDEN)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Log the user in
            login(request, user)

            # Prepare response
            return Response({
                "message": "Admin login successful",
                "user_id": user.id,
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Catch any unexpected errors
            logger.error(f"Unexpected error during admin login: {str(e)}")
            return Response({
                "error": "An unexpected error occurred"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        # Add some logging to help diagnose issues
        print(f"Login attempt for username: {username}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Ensure the user is an admin
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                login(request, user)
                return Response({
                    "message": "Admin logged in successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Only admins can log in here"}, status=status.HTTP_403_FORBIDDEN)
        
        # More detailed error logging
        print("Authentication failed")
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Ensure the user is an admin
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                login(request, user)
                return Response({
                    "message": "Admin logged in successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Only admins can log in here"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


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

# Recipe views
class CreateRecipeView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Important for file uploads

    def get_queryset(self):
        user = self.request.user
        return Recipes.objects.filter(author=user)

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
    permission_classes = [AllowAny]
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
