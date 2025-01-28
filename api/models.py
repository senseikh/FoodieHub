from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Extended User model
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/pictures", null=True, blank=True)
    website = models.URLField(blank=True, null=True)


# Recipe model
class Recipes(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    image = models.ImageField(upload_to="recipes/images", null=True, blank=True)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="recipe_categories"
    )
    tags = models.ManyToManyField("Tag", blank=True, related_name="recipe_tags")
    is_public = models.BooleanField(default=False)  # To determine if the recipe is shareable

    def __str__(self):
        return self.title


# Category model
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Comment model
class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name="recipe_comments"  # Unique related_name
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"


# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


# Blog model
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_blogs"  # Unique related_name
    )
    is_public = models.BooleanField(default=True)  # Blogs are public by default

    def __str__(self):
        return self.title
