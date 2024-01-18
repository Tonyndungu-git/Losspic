from django import forms
from .models import CompressedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = CompressedImage
        fields = ['original_image']