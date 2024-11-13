from django import forms
from .models import Chord

class ChordVerificationForm(forms.Form):
    chord_name = forms.CharField(max_length=100, label="Chord Name")
    notes = forms.CharField(max_length=100, label="Notes")

class ChordSearchForm(forms.Form):
    custom_input_frets = forms.CharField(max_length=100)
    
class ChordForm(forms.ModelForm):
    class Meta:
        model = Chord
        fields = ('user', 'name', 'base', 'frets', 'fingers')

