from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Recipes, Category, Tag, Comment, UserProfile


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# UserProfile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'website']


# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# Tag serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


# Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'user', 'content', 'created_at', 'updated_at']
        extra_kwargs = {"recipe": {"read_only": True}}


# Recipe serializer
class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'image', 'category', 'tags', 'comments']
        extra_kwargs = {"author": {"read_only": True}}
        read_only_fields = ['author']
