from django.urls import path
from .views import home, compress_image
app_name = 'backend'

urlpatterns = [
    path('', home, name='home'),
    path('compress/', compress_image, name='compress_image')
]
