from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    re_path(r'^chords/create/$', views.chord_create, name='chord_create'),
    re_path(r'^chords/(?P<id>\d+)/delete/$', views.chord_delete, name='chord_delete'),
]