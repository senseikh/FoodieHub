
from django.contrib import admin
from .models import Hotel,Resource,Restaurant

# Register your models here.
admin.site.register(Resource)
admin.site.register(Hotel)
admin.site.register(Restaurant)