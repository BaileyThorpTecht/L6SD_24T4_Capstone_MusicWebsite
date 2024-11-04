from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord
import json
from musicwebsite.forms import ChordVerificationForm
from .forms import ChordSearchForm
import logging
from django.views.decorators.csrf import csrf_exempt


# The views.
def index(request):
    context = {
        "context_name" : "context data"
    }
    return render(request, 'musicwebsite/index.html', context)

logger = logging.getLogger(__name__)

# This view is what process user input into searching the JSON file in the database for related chord
@csrf_exempt  # Exempt from CSRF in development; remove in production if using CSRF protection
def chord_search(request):
    if request.method != 'POST':
        return JsonResponse({"Error": "POST request required."}, status=405)

    # Step 1: Parse JSON input
    try:
        data = json.loads(request.body)
        user_frets_list = data.get('frets')  # Expects 'frets' as a JSON key with array of integers
        if not user_frets_list or not all(isinstance(fret, int) for fret in user_frets_list):
            return JsonResponse({"Error": "Invalid input. 'frets' should be an array of integers."}, status=400)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"Error": "Invalid JSON input."}, status=400)

    # Step 2: Prepare a list to store matching chords
    matching_chords = []

    # Step 3: Iterate over each chord in the database
    for chord in Chord.objects.all():
        # Check if the chord frets length matches the user input length
        if len(chord.frets) != len(user_frets_list):
            continue

        # Calculate adjusted frets by adding 'base' to each fret in chord.frets
        adjusted_frets = [fret + chord.base if fret != -1 else -1 for fret in chord.frets]

        # Adjust user input to various offsets for comparison
        adjusted_user_frets = [
            [fret + offset if fret != -1 else -1 for fret in user_frets_list]
            for offset in range(1, 6)  # Create 5 variations of offsets from +1 to +5
        ]

        # Compare user inputted frets with adjusted frets for each offset
        if any(adjusted_user_frets_offset == adjusted_frets for adjusted_user_frets_offset in adjusted_user_frets):
            matching_chords.append({
                "name": chord.name,
                "base": chord.base,
                "original_frets": chord.frets,
                "fingers": chord.fingers,
            })
            break  # Stop after the first match; remove `break` if you want multiple matches

    # Step 4: Return the result as JSON
    return JsonResponse({"matching_chords": matching_chords})




