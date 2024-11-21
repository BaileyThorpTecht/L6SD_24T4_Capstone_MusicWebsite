from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.forms import UserRegisterForm
from django.contrib import messages
from . import forms
from django.http import HttpResponseForbidden
from django.core.mail import send_mail

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
    user = request.user
    
    if request.method == "POST":
        # Delete user account and related data
        # You can delete associated models (e.g., posts, profile, etc.)
        user.profile.delete()  # Example if you have a related Profile model
        user.posts.all().delete()  # Example if user has posts

        # Delete the user account
        user.delete()

        # Send a confirmation email (optional)
        send_mail(
            'Account Deletion Confirmation',
            'Your account has been permanently deleted. We are sorry to see you go!',
            'your-email@example.com',  # Replace with your email
            [user.email],
            fail_silently=False,
        )

        # Log the user out after deletion
        logout(request)

        # Redirect to a confirmation page
        return redirect("account_deleted")  # Change to a confirmation page URL

    return render(request, 'delete_account.html', {'user': user})


from django.shortcuts import render

def account_deleted(request):
    return render(request, 'account_deleted.html')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def FAQ(request):
    return render(request, 'FAQ.html')
