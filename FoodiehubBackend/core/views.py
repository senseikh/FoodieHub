from rest_framework import generics
from .models import  User, Recipe
from .serializers import  UserSerializer, RecipeSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import  status
from django.db import DatabaseError
from django.db.utils import OperationalError

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class Register(generics.CreateAPIView):
    """
        User registration
    """
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email', None)
            username = request.data.get('username', None)
            password = request.data.get('password', None)
            if email and User.objects.filter(email=email).exists():
                return Response({
                    "status": "failed", 
                    "message": "Email is already registered. Please use a different email."
                    },   status=status.HTTP_400_BAD_REQUEST)
            if username and User.objects.filter(username=username).exists():
                return Response({
                    "status": "failed", 
                    "message": "Username is already taken. Please choose a different username."
                    },   status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                # send_welcome_email(user)
                return Response({
                    "status": "success", 
                    "message":"Registration successful. Verification  email sent to your email.",
                    },
                    status=status.HTTP_201_CREATED)
            # db connection issues?. get..
        except Exception as e:  
            return Response({
                "status": "failed",
                "message": "Internal server error. Failed to save"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)