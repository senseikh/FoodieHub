from django.contrib import admin
from .models import Recipes,Category,Comment,Tag, Blog

# Register your models here.
admin.site.register(Recipes)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Blog)
# admin.site.register(UserProfile)