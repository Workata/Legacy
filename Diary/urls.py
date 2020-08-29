from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name= 'home'),
    path('anime', views.anime, name='anime'),
    path('animeList', views.animeList, name = 'animeList'),
    path('animeAdd', views.animeAdd, name = 'animeAdd'),
    path('listModify', views.listModify, name='listModify'),
    path('sortStatus', views.sortStatus, name='sortStatus'),
    path('sortTitle', views.sortTitle, name='sortTitle'),
    path('sortEndDate', views.sortEndDate, name='sortEndDate'),
    path('sortPremiered', views.sortPremiered, name='sortPremiered'),
    path('index', views.index, name='index'),
    path('animeInfo', views.animeInfo, name='animeInfo'),
    path('animeDelete', views.animeDelete, name='animeDelete')
]