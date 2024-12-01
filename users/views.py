from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegisterForm, MemberForm, Member
from .tasks import send_registration_confirmation
from django.contrib import messages
from . import forms
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import requests

# Create your views here.

# Registration
def register_page(request):
    if request.method == "POST":
        recaptcha_token = request.POST.get('recaptcha_token')
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {
            'secret' : settings.REGISTER_RECAPTCHA_PRIVATE_KEY,
            'response' : recaptcha_token
        }
        recaptcha_response = requests.post(recaptcha_url, data = recaptcha_data).json()
        
        if not recaptcha_response.get('success', False):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return render(request, 'register.html', {'form' : UserRegisterForm()})
        
        # Proceed with the registration process
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Member.objects.create(user = user)
            send_registration_confirmation.delay(user.id)
            return redirect('home')
        else:
            form = UserRegisterForm()
            return render(request, 'register.html', {'form' : form})
    else:
        form = UserRegisterForm()
        return render(request, 'register.html', {'form' : form})


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

@login_required()
def accountSettings(request):
    try:
        member = request.user.member
    except Member.DoesNotExist:
        member = Member.objects.create(user=request.user)  # Create a Member object if it doesn't exist
    
    form = MemberForm(instance=member)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
    
    context = {'form': form}
    return render(request, 'users/account-settings.html', context)

def some_view(request):
    member = request.user.member
    profile_pic_url = member.profile_pic.url if member.profile_pic else '/static/images/profile-pic-fallback.png'
    return render(request, 'template.html', {'profile_pic_url': profile_pic_url})


# @login_required
# def delete_account(request):
#     user = request.user
#     # Mark user for deletion (soft delete) by setting an 'is_active' field to False
#     user.is_active = False
#     user.deleted_at = timezone.now() # Optional: adding a timestamp for soft delete.
    
#     # Log the user out after marking for deletion
#     logout(request)
#     messages.success(request, "Your account has been marked for deletion.")
    
#     return redirect('home')  # Redirects to the homepage or another view



@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return redirect('profile')
