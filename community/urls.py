from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    HotelViewSet, RestaurantViewSet, 
    CommunityPostViewSet, ResourceViewSet
)

# Define a router for standard CRUD viewsets
router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'community-posts', CommunityPostViewSet, basename='communitypost')
router.register(r'resources', ResourceViewSet, basename='resource')

urlpatterns = [
    # Hotel-related paths
    path('hotels/nearby/', HotelViewSet.as_view({'get': 'nearby'}), name='hotel-nearby'),
    path('restaurants/nearby/', RestaurantViewSet.as_view({'get': 'nearby'}), name='restaurant-nearby'),
    path('community-posts/<int:pk>/like/', CommunityPostViewSet.as_view({'post': 'like'}), name='community-post-like'),
] + router.urls
