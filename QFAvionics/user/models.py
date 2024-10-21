from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    address = models.TextField(blank=True, null=True, default='')  
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return self.username 
    

    

    

