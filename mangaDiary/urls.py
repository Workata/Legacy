from django.urls import path
from . import views


urlpatterns = [
    path('mangaList', views.mangaList, name = 'mangaList'),
    path('mangaAdd', views.mangaAdd, name = 'mangaAdd'),
    path('mangaListModify', views.mangaListModify, name='mangaListModify'),
    path('mangaInfo', views.mangaInfo, name='mangaInfo'),
    path('mangaDelete', views.mangaDelete, name='mangaDelete')
]