from django.urls import path, include
from .views import NearbyHotelsView

# Custom URLs combined with router URLs
urlpatterns = [
    path('nearby-hotels/', NearbyHotelsView.as_view(), name='nearby-hotels'),
]
