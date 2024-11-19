from django.urls import path
from . import views

urlpatterns = [
    path("recipe/", views.CreateRecipeView.as_view(), name="recipe creattion"),
    path("recipe/delete/<int:pk>/", views.RecipeDelete.as_view(), name="Recipe deletion"),
]