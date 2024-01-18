from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from matplotlib.image import imread
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from .models import CompressedImage

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'pages/home.html')


def compress_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            original_image = form.cleaned_data['original_image']
            
            # Perform SVD compression
            A = imread(original_image.file)  # Access file content directly
            X = np.mean(A, -1)
            U, S, VT = np.linalg.svd(X, full_matrices=False)
            S = np.diag(S)

            # Choose compression level (r value)
            r = 100
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