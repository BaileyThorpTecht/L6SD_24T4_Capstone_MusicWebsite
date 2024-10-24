from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from musicwebsite.models import Chord
from musicwebsite.forms import ChordVerificationForm


def index(request):
    context = {
        "context_name" : "context data"
    }
    return render(request, 'musicwebsite/index.html', context)


def verify_chord(request):
    message = None
    if request.method == "POST":
        form = ChordVerificationForm(request.POST)
        if form.is_valid():
            chord_name = form.cleaned_data['chord_name']
            notes = form.cleaned_data['notes']
        

        try:
            chord = Chord.objects.get(name=chord_name)

            if chord.notes == notes:
                message = f"Success! The Chord '{chord_name}' is correctly identified."
            else:
                message = f"Chord '{chord_name}' found, but the notes do not match."
        except Chord.DoesNotExist:
            message = f"Chord '{chord_name}' not found in the database."
        
    else:
        form = ChordVerificationForm()

    return render(request, 'verify_chord.html', {'form': form, 'message': message})




