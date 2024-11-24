from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing-page"),
    path("index/", views.index, name="home"),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    re_path(r'^chords/load/$', views.chord_load, name='chord_load'),
    re_path(r'^chords/create/$', views.chord_create, name='chord_create'),
    re_path(r'^chords/(?P<id>\d+)/delete/$', views.chord_delete, name='chord_delete'),
]