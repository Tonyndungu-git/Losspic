
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from rest_framework.decorators import api_view, permission_classes
from .forms import ImageCompressionForm

def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context = {
        "form": form,
        "btn_label": "Login",
        "title": "Login"
    }
    return render(request, "accounts/auth.html", context)

def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Click to Confirm",
        "title": "Logout"
    }
    return render(request, "accounts/auth.html", context)

def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        # send a confirmation email to verify their account
        login(request, user)
        return redirect("/")
    context = {
        "form": form,
        "btn_label": "Register",
        "title": "Register"
    }
    return render(request, "accounts/auth.html", context)
def home(request):
    return render(request, 'pages/home.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageCompressionForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import CompressedImage
from matplotlib.image import imread
import numpy as np
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from PIL import Image
import matplotlib.pyplot as plt
from rest_framework.permissions import IsAuthenticated
from .forms import ImageUploadForm

# Import other necessary modules

@permission_classes([IsAuthenticated])
def compress_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            original_image = form.cleaned_data['original_image']

            # # Check if the uploaded file is in PNG format
            # try:
            #     Image.open(original_image.file)
            # except Exception as e:
            #     return HttpResponse("Error: The uploaded image is not in PNG format.")

            # Perform SVD compression
            A = imread(original_image.file)  # Access file content directly
            X = np.mean(A, -1)
            
            if X.ndim == 3:  # Check if X is a 3D array (RGB image)
                X = np.mean(X, -1)  # Convert RGB to grayscale
            
            U, S, VT = np.linalg.svd(X, full_matrices=False)
            S = np.diag(S)

            # Choose compression level (r value)
            r = 75
            Xapprox = U[:, :r] @ S[0:r, :r] @ VT[:r, :]

            # Save the compressed image
            buffer = BytesIO()
            plt.imsave(buffer, Xapprox, cmap='gray', format='png')
            compressed_image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            compressed_image = ContentFile(base64.b64decode(compressed_image_data), name='compressed_image.png')

            # Save the compressed image data to the model
            compressed_image_instance = CompressedImage(original_image=original_image)
            compressed_image_instance.compressed_image.save('compressed_image.png', compressed_image)
            compressed_image_instance.save()

            # Provide the compressed image for download
            response = HttpResponse(compressed_image_instance.compressed_image.file, content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename={original_image.name}_compressed.png'
            return response

    else:
        form = ImageUploadForm()

    return render(request, 'image_compressor/compress_image.html', {'form': form})