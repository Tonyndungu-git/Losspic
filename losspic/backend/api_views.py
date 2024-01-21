from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageCompressionSerializer
from matplotlib.image import imread
import numpy as np
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from .models import CompressedImage
from PIL import Image
import matplotlib.pyplot as plt
from rest_framework.permissions import IsAuthenticated


class ImageCompressionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Step 1: Deserialize the incoming data using the serializer
        serializer = ImageCompressionSerializer(data=request.data)

        # Step 2: Validate the deserialized data
        if serializer.is_valid():
            # Step 3: Extract validated data
            original_image = serializer.validated_data['original_image']

            # Step 4: Your existing image compression logic here...
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
            response_data = {
                'message': 'Image compressed successfully',
                'compressed_image_url': compressed_image_instance.compressed_image.url,
            }

            # Step 5: Return a response with the result data and a 200 OK status
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Step 6: If the data is not valid, return an error response with the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
