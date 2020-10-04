from django.urls import path
from . import views


urlpatterns = [
   path('exportManga', views.exportManga, name = 'exportManga'),
   path('importManga', views.importManga, name = 'importManga')
]