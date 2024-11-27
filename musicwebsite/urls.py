from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing-page"),
    path("index/", views.index, name="home"),
    re_path(r'^chords/read/$', views.chord_read, name='chord_read'),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    re_path(r'^chords/load/$', views.chord_load, name='chord_load'),
    re_path(r'^chords/create/$', views.chord_create, name='chord_create'),
    re_path(r'^chords/(?P<id>\d+)/delete/$', views.chord_delete, name='chord_delete'),
    re_path(r'^songs/create$', views.song_create, name='song_create'),
    re_path(r'^songs/load$', views.song_load, name='song_load'),
    re_path(r'^songs/update$', views.song_update, name='song_update'),
    re_path(r'^chords/(?P<id>\d+)/songs/update$', views.song_update_from_chords, name='song_update_from_chords'),
    re_path(r'^songs/delete$', views.song_delete, name='song_delete'), #deletes entire song
    re_path(r'^songs/(?P<id>\d+)/remove/$', views.song_remove, name='song_remove'), #deletes songchord from song
    re_path(r'^songs/play/$', views.song_play, name='song_play'),
    
]