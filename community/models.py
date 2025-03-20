from django.db import models
from api.models import User 

from api.models import models
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotels', default=1)

    def __str__(self):
        return self.name
