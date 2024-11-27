from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.forms import UserRegisterForm
from .tasks import send_registration_confirmation
from django.contrib import messages
from . import forms
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

# Create your views here.

# Registration
def register_page(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_registration_confirmation.delay(user.id)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', { 'form' : form })


# Login
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', { 'form': form })


# Logout
def logout_page(request):
    logout(request)
    return redirect('home')


# Profile
@login_required()
def profile_page(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('login')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return redirect('profile')
