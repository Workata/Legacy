from django.urls import path
from . import views


urlpatterns = [
   path('mangaScraper', views.mangaScraper, name = 'mangaScraper')
]