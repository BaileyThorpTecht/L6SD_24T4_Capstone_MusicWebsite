from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('delte-account/', views.delete_account, name='delete_account'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset-password.html"), name="reset-password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="reset-password-done.html"), name="reset-password-done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset-password-form.html"), name="reset-password-confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset-password-complete.html"), name="reset-password-complete"),
    path('', include('django.contrib.auth.urls')),
]
