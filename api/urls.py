from django.urls import path,include
from . import views
from .models import User 
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CreateUserView,
    CategoryListCreateView,
    CategoryDetailView,
    TagListCreateView,
    TagDetailView,
    CommentListCreateView,
    CommentDeleteView,
    RecipeDetailView,
    RecipeUpdateView,
    AdminLoginView,
    BlogListView,
    BlogDetailView,
    SharedRecipeListView,
    UpdateUserProfileView,
    ChangePasswordView,
    BlogListView,
    BlogUpdateDeleteView,
    MyBlogsView,
    UserProfileView,
    PublicRecipesView,
)
urlpatterns = [

 # User creation and authentication
    path('user/register/', CreateUserView.as_view(), name="register"),
    path("login/user/", views.UserLoginView.as_view(), name="user-login"),
    path("login/admin/", AdminLoginView.as_view(), name="admin-login"),

    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UpdateUserProfileView.as_view(), name='update-profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/users/', views.AdminUserManagementView.as_view(), name='admin-user-management'),
    path('admin/users/<int:user_id>/', views.AdminUserManagementView.as_view(), name='admin-user-toggle'),

    # Blog URLs
    path("blogs/", BlogListView.as_view(), name="list_blogs"),
    path("blogs/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path('blogs/my-blogs/', MyBlogsView.as_view(), name='my-blogs'),
    path('blogs/<int:pk>/', BlogUpdateDeleteView.as_view(), name='blog-detail'),
   

    # Recipe Urls
    path("recipe/", views.CreateRecipeView.as_view(), name="recipe creattion"),
    path("recipe/list/", views.CreateRecipeView.as_view(), name="recipe creattion"),
    
    path("recipe/delete/<int:pk>/", views.RecipeDelete.as_view(), name="Recipe deletion"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipes/<int:pk>/update/", RecipeUpdateView.as_view(), name="recipe_update"),
    path('recipes/public/', PublicRecipesView.as_view(), name='public_recipes'),

    

    path("categories/", CategoryListCreateView.as_view(), name="list_create_categories"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("tags/", TagListCreateView.as_view(), name="list_create_tags"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag_detail"),
    path("recipes/<int:recipe_id>/comments/", CommentListCreateView.as_view(), name="list_create_comments"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="delete_comment"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)