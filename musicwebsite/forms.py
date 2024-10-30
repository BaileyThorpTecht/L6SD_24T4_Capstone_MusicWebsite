from django import forms

class ChordVerificationForm(forms.Form):
    chord_name = forms.CharField(max_length=100, label="Chord Name")
    notes = forms.CharField(max_length=100, label="Notes")
