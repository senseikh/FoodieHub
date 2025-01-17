from django.urls import path
from . import views
from .views import (
    CreateUserView,
    CreateRecipeView,
    RecipeDelete,
    RecipeListView,
    CategoryListCreateView,
    CategoryDetailView,
    TagListCreateView,
    TagDetailView,
    CommentListCreateView,
    CommentDeleteView,
)

urlpatterns = [
    path("users/", CreateUserView.as_view(), name="create_user"),
    path("recipe/", views.CreateRecipeView.as_view(), name="recipe creattion"),
    path("recipe/delete/<int:pk>/", views.RecipeDelete.as_view(), name="Recipe deletion"),
    path("recipes/list/", RecipeListView.as_view(), name="list_recipes"),
    path("categories/", CategoryListCreateView.as_view(), name="list_create_categories"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("tags/", TagListCreateView.as_view(), name="list_create_tags"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag_detail"),
    path("recipes/<int:recipe_id>/comments/", CommentListCreateView.as_view(), name="list_create_comments"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="delete_comment"),
]