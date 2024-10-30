from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord
from musicwebsite.forms import ChordVerificationForm
from .forms import ChordSearchForm


# The views.
def index(request):
    context = {
        "context_name" : "context data"
    }
    return render(request, 'musicwebsite/index.html', context)

# This view is what process user input into searching the JSON file in the database for related chord
def chord_search(request):
    form = ChordSearchForm()
    results = None

    if request.method == 'POST':
        form = ChordSearchForm(request.POST)
        if form.is_valid():
            frets_input = form.cleaned_data['frets']
            frets_list = [int(f) for f in frets_input.split(',')]

            # Search for chords that match the frets
            results = Chord.objects.filter(frets=frets_list)

    return render(request, 'chords/search.html', {'form': form, 'results': results})




