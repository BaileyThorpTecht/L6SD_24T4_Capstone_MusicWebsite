from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord
from musicwebsite.forms import ChordVerificationForm
from .forms import ChordSearchForm
import logging


# The views.
def index(request):
    context = {
        "context_name" : "context data"
    }
    return render(request, 'musicwebsite/index.html', context)

logger = logging.getLogger(__name__)

# This view is what process user input into searching the JSON file in the database for related chord
def chord_search(request):
    # Step 1: Get the user input for 'frets'
    user_frets_input = request.GET.get('frets')
    
    if not user_frets_input:
        return JsonResponse({"Error": "No frets input provided."}, status=400)
    
    # Step 2: Convert the input string to a list of integers
    try:
        user_frets_list = list(map(int, user_frets_input.split(',')))
    except ValueError:
        return JsonResponse({"Error": "Invalid frets format. Expected a comma-separated list of integers."}, status=400)

    # Step 3: Prepare a list to store matching chords
    matching_chords = []
    
    # Step 4: Iterate over each chord in the database
    for chord in Chord.objects.all():
        # Check if the chord frets length matches the user input length
        if len(chord.frets) != len(user_frets_list):
            continue

        # Calculate adjusted frets by adding 'base' to each fret in chord.frets
        adjusted_frets = [fret + chord.base if fret != -1 else -1 for fret in chord.frets]

        # Adjust user input to remove the base value for comparison
        adjusted_user_frets1 = [fret + 1 if fret != -1 else -1 for fret in user_frets_list]
        adjusted_user_frets2 = [fret + 2 if fret != -1 else -1 for fret in user_frets_list]
        adjusted_user_frets3 = [fret + 3 if fret != -1 else -1 for fret in user_frets_list]
        adjusted_user_frets4 = [fret + 4 if fret != -1 else -1 for fret in user_frets_list]       
        adjusted_user_frets5 = [fret + 5 if fret != -1 else -1 for fret in user_frets_list] 

        # Compare user inputted frets with adjusted frets
        if adjusted_user_frets1 == adjusted_frets:
            # If they match, add the chord to the list of matching chords
            matching_chords.append({
                "name": chord.name,
                "base": chord.base,
                "original_frets": chord.frets,
                "fingers": chord.fingers,
            })
            break
        elif adjusted_user_frets2 == adjusted_frets:
            # If they match, add the chord to the list of matching chords
            matching_chords.append({
                "name": chord.name,
                "base": chord.base,
                "original_frets": chord.frets,
                "fingers": chord.fingers,
            })
            break
        elif adjusted_user_frets3 == adjusted_frets:
            # If they match, add the chord to the list of matching chords
            matching_chords.append({
                "name": chord.name,
                "base": chord.base,
                "original_frets": chord.frets,
                "fingers": chord.fingers,
            })
            break
        elif adjusted_user_frets4 == adjusted_frets:
            # If they match, add the chord to the list of matching chords
            matching_chords.append({
                "name": chord.name,
                "base": chord.base,
                "original_frets": chord.frets,
                "fingers": chord.fingers,
            })
            break
        elif adjusted_user_frets5 == adjusted_frets:
            # If they match, add the chord to the list of matching chords
            matching_chords.append({
                "name": chord.name,
                "base": chord.base,
                "original_frets": chord.frets,
                "fingers": chord.fingers,
            })
            break

    return render(request, 'musicwebsite/index.html')




