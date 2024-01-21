from django.db import models
from django.conf import settings
# from django.contrib.auth.models import AbstractUser

# Create your models here.

User = settings.AUTH_USER_MODEL

class CompressedImage(models.Model):
    original_image = models.ImageField(upload_to='images/')
    compressed_image = models.ImageField(upload_to='compressed_images/', blank=True, null=True)


# class CustomUser(AbstractUser):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     country = models.CharField(max_length=255)

#     def __str__(self):
#         return self.username

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username