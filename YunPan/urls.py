from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'YunPan'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload'),
    path('public/', views.public, name='public'),
    path('private/', views.private, name='private'),
    path('file/<int:pk>/', views.download_file, name='file'),
    path('download/<int:pk>/', views.download_private_file, name='download'),
    path('move/<int:pk>/', views.change_file_type, name='move'),
    path('delete/<int:pk>/', views.delete_file, name='delete'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
