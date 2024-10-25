# fichier/urls.py
from django.urls import path
from . import views
from .views import process_character_file

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('process-character/', views.process_character_file, name='process_character_file'),
]
