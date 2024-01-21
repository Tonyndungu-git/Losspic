from django.urls import path
from .api_views import ImageCompressionAPIView
from .views import login_view, logout_view, register_view


urlpatterns = [
    path('compress_image/', ImageCompressionAPIView.as_view(), name='api_compress_image'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
