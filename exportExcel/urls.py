from django.urls import path
from . import views


urlpatterns = [
   path('exportAnime', views.exportAnime, name = 'exportAnime'),
   path('importAnime', views.importAnime, name = 'importAnime')
]