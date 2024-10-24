from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.forms import UserRegisterForm
from django.contrib import messages
from . import forms

# Create your views here.
def register_page(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', { 'form' : form })

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', { 'form': form })

def logout_page(request):
    logout(request)
    return redirect('home')

@login_required()
def profile_page(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('login')
