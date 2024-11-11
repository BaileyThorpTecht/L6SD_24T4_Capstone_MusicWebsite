from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('chords/create/', views.chord_create, name='chord_create'),
]