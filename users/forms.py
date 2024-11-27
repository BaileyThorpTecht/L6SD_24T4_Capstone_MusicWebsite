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
    agree_to_terms = forms.BooleanField(
        required=True,
        label=mark_safe('I agree to the <a href="#" data-bs-toggle="modal" data-bs-target="#termsModal">Terms & Conditions</a>'),
        widget=forms.CheckboxInput(attrs={
            'id' : 'termsCheckbox',
            'onclick' : 'toggleRegisterButton()'
            })
    )
    agree_to_privacy = forms.BooleanField(
        required=True,
        label=mark_safe('I agree to the <a href="#" data-bs-toggle="modal" data-bs-target="#privacyModal">Privacy Policy</a>'),
        widget=forms.CheckboxInput(attrs={
            'id' : "privacyCheckbox",
            'onclick' : 'toggleRegisterButton()'
            })
    )
    captcha = ReCaptchaField(widget = ReCaptchaV2Checkbox)     
    
        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MemberForm(ModelForm):
    
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['user']