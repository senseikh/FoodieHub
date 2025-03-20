from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Hotel
from .serializers import HotelSerializer
from api.models import User 
class NearbyHotelsView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    # authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        if lat and lng:
            return Hotel.objects.filter(
                latitude__gte=float(lat) - 0.05,
                latitude__lte=float(lat) + 0.05,
                longitude__gte=float(lng) - 0.05,
                longitude__lte=float(lng) + 0.05
            )
        return Hotel.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
