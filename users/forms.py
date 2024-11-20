from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    agree_to_terms = forms.BooleanField(required=True, label="I agree to the Terms & Conditions")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']