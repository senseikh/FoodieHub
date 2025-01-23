
from django.contrib import admin
from django.shortcuts import render
from django.urls import path,include
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='get token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="refresh tooken"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
