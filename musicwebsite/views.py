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
    # Retrieve the 'frets' input from the query parameters
    frets_input = request.GET.get('frets')
    
    if not frets_input:
        return JsonResponse({"error": "No frets input provided."}, status=400)
    
    # Convert the input string to a list of integers (e.g., "0,3,2,0,1,0" to [0, 3, 2, 0, 1, 0])
    try:
        frets_input_list = list(map(int, frets_input.split(',')))
    except ValueError:
        return JsonResponse({"error": "Invalid frets format. Please make sure they are all numbers seperatd commas."}, status=400)

    # Search for chords with matching frets
    matching_chords = Chord.objects.filter(frets=frets_input_list)
    
    # Create a response list with the matching chords
    chord_list = [
        {
            "name": chord.name,
            "base": chord.base,
            "frets": chord.frets,
            "fingers": chord.fingers,
        }
        for chord in matching_chords
    ]
    
    # Return the response as JSON
    return JsonResponse({"chords": chord_list})




