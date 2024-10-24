from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset-password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="reset-password-sent"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="reset-password-complete"),
]
