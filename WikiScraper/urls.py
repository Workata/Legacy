from django.urls import path
from . import views


urlpatterns = [
   path('animeScraper', views.animeScraper, name = 'animeScraper')
]