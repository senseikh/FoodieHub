from django.urls import path
from .views import RecipeListCreateView, Register

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('api/recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
]
