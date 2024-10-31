from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path('search/', views.chord_search, name='chord_search'),
]