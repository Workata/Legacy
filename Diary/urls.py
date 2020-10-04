# TODO rename this app to animeDiary
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name= 'home'),
    path('animeList', views.animeList, name = 'animeList'),
    path('animeAdd', views.animeAdd, name = 'animeAdd'),
    path('animeListModify', views.animeListModify, name='animeListModify'),
    path('animeInfo', views.animeInfo, name='animeInfo'),
    path('animeDelete', views.animeDelete, name='animeDelete')
]