from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import terms_and_conditions, privacy_policy, FAQ, terms_and_conditions_footer, privacy_policy_footer, community_guidelines, contact_us



urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset-password.html"), name="reset-password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="reset-password-done.html"), name="reset-password-done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset-password-form.html"), name="reset-password-confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset-password-complete.html"), name="reset-password-complete"),
    path('terms-and-conditions/', terms_and_conditions, name='terms_and_conditions'),
    path('terms-and-conditions-footer/', terms_and_conditions_footer, name='terms_and_conditions_footer'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('privacy-policy-footer/', privacy_policy_footer, name='privacy_policy_footer'),
    path('community-guidelines/', community_guidelines, name='community_guidelines'),
    path('F-A-Q/', FAQ, name='FAQ'),
    path('contact-us/', contact_us, name='contact-us'),
    path('', include('django.contrib.auth.urls')),
]
