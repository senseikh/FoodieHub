from rest_framework import serializers
from .models import BlogPost

class BlogPostPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'status']
