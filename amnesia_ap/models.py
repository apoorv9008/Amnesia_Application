from django.db import models
from django.utils import timezone

class User(models.Model):
    name         = models.CharField( max_length=50 )
    phone_number = models.CharField( max_length=15 )
    created 	 = models.DateTimeField(auto_now_add=True)
