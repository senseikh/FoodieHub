from rest_framework import serializers
from .models import Hotel, Restaurant, CommunityPost, Resource

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class CommunityPostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = CommunityPost
        fields = '__all__'

    def get_author_name(self, obj):
        return obj.author.username

    def get_likes_count(self, obj):
        return obj.likes.count()

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'