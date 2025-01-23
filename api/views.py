from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics,status
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
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
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  # Ensure it's an admin
                login(request, user)
                return Response({"message": "Admin logged in successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Only admins can log in here"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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
