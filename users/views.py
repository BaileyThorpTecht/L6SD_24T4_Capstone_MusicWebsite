from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegisterForm, MemberForm, Member
from django.contrib import messages
from django.contrib.auth.models import User

# Registration
def register_page(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Member.objects.create(user=user)
            messages.success(request, "Registration successful!")
            return redirect('login')
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

# Login
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout
def logout_page(request):
    logout(request)
    return redirect('home')

# Profile
@login_required()
def profile_page(request):
    return render(request, 'profile.html')

# @login_required()
# def accountSettings(request):
#     member = request.user.member
#     form = MemberForm(instance=member)
    
#     if request.method == 'POST':
#         form = MemberForm(request.POST, request.FILES, instance=member)
#         if form.is_valid():
#             form.save()
    
#     context = {'form': form}
#     return render(request, 'users/account-settings.html', context)

@login_required()
def accountSettings(request):
    member = request.user.member
    user = request.user 
    member_form = MemberForm(instance=member)
    
    if request.method == 'POST':
        member_form = MemberForm(request.POST, request.FILES, instance=member)
        if member_form.is_valid():
            member_form.save()

        # Update User fields (username and email)
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()
    
    context = {'form': member_form, 'user': user, 'member': member}
    return render(request, 'users/account-settings.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return redirect('profile')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def terms_and_conditions_footer(request):
    return render(request, 'terms_and_conditions_footer.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def privacy_policy_footer(request):
    return render(request, 'privacy_policy_footer.html')

def FAQ(request):
    return render(request, 'FAQ.html')

def community_guidelines(request):
    return render(request, 'community_guidelines.html')

def contact_us(request):
    return render(request, 'contact_us.html')
