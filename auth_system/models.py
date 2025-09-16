from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    birsth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
