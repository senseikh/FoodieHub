from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class User(AbstractUser):
    is_chef = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_user_set',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_permissions_set',
    )

    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=12, blank=True)
    email_is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    
    def generate_verification_token(self):
        token_generator = PasswordResetTokenGenerator()
        self.verification_token = token_generator.make_token(self)
        self.save()
        return self.verification_token
    
    def __str__(self):
        return self.username
  

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    ratings = models.FloatField(default=0.0)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
