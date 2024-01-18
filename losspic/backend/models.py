from django.db import models

# Create your models here.

class CompressedImage(models.Model):
    original_image = models.ImageField(upload_to='images/')
    compressed_image = models.ImageField(upload_to='compressed_images/', blank=True, null=True)
