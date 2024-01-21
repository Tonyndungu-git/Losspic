from django import forms
from .models import CompressedImage, CustomUser

class ImageCompressionForm(forms.Form):
    original_image = forms.ImageField()

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = CompressedImage
        fields = ['original_image']

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
