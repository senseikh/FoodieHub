from django.urls import path
from . import views

urlpatterns = [
    path('api/posts/', views.BlogPostListCreate.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', views.BlogPostDetail.as_view(), name='post_detail'),
]
