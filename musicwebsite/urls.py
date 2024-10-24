from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('verify-chord/', views.verify_chord, name='verify_chord'),  
]