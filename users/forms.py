from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.safestring import mark_safe
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    captcha = ReCaptchaField(widget = ReCaptchaV2Checkbox)     
    
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MemberForm(ModelForm):
    
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user']