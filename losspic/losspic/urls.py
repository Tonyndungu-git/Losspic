# main urls.py
from django.contrib import admin
from django.urls import path, include
from backend.views import home
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('image_compressor/', include('backend.urls')),
    path('', include('backend.api_urls')),
    path('', home, name='home'),
]
