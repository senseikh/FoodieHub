# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Recipes, Category, Tag, Comment, Blog,User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


from .models import User 
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validate password strength
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
            
        return data

    def create(self, validated_data):
        # Remove confirm_password from the data
        validated_data.pop('confirm_password', None)
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email',
            'username',
            'bio',
            'profile_picture',
            'website',
            'date_joined',
            'first_name',
            'last_name'
        ]
        read_only_fields = ['id', 'email', 'date_joined']  # Make certain fields read-only for security

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['profile_picture']:
            representation['profile_picture'] = self.context['request'].build_absolute_uri(instance.profile_picture.url)
        return representation

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
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'image', 'category', 'tags', 'comments', 'is_public']
        extra_kwargs = {"author": {"read_only": True}}
        read_only_fields = ['author']
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'image', 'title', 'content', 'created_at', 'updated_at', 'author', 'is_public']

        extra_kwargs = {"author": {"read_only": True}}
        read_only_fields = ['author']
        
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None