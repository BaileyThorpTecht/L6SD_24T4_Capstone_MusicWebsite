from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord
from musicwebsite.forms import ChordVerificationForm

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from json import dumps, loads
from json import dump
import json

from .forms import ChordSearchForm



# The views.
@csrf_exempt
def index(request):
    if request.method == 'POST':
        # Handle the chord-saving action
        data = loads(request.body)
        frets = data.get('frets', '')
        if frets:
            Chord.objects.create(frets=frets)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)

    # Handle the initial page load
    chordList = list(Chord.objects.all())
    dictList = [model_to_dict(chord) for chord in chordList]
    dataJSON = dumps(dictList, cls=DjangoJSONEncoder)  # JSON serialize the chord data for JavaScript

    context = {
        'data': dataJSON,
        'chords': chordList,  # Pass chords directly for any Django template use
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





