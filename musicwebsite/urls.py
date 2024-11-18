from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    re_path(r'^chords/load/$', views.chord_load, name='chord_load'),
    re_path(r'^chords/create/$', views.chord_create, name='chord_create'),
    re_path(r'^chords/(?P<id>\d+)/delete/$', views.chord_delete, name='chord_delete'),
    re_path(r'^songs/create$', views.song_create, name='song_create'),
    re_path(r'^songs/(?P<id>\d+)/load$', views.song_load, name='song_load'),
    re_path(r'^songs/(?P<id>\d+)/update$', views.song_update, name='song_update'),
    re_path(r'^songs/(?P<id>\d+)/delete$', views.song_delete, name='song_delete'),
]