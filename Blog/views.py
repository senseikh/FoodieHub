from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostPostSerializer

# List all blog posts or create a new one
class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.filter(status=True).order_by('-created_at')
    serializer_class = BlogPostPostSerializer

# Retrieve, update, or delete a specific blog post
class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.filter(status=True)
    serializer_class = BlogPostPostSerializer
