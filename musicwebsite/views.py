from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Chord, User

from django.core import serializers
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from json import dumps, loads

import pdb

from .forms import ChordForm



# The views.
def index(request):
    
    chordList = list(Chord.objects.all())

    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))    
    
    dataJSON = dumps(dictList)
    
    context = {
        'data' : dataJSON,
        'chords' : Chord.objects.all() #if this isnt here, then the page loads to quickly and the first ajax request to load the custom chords happens before the database is loaded and it fails to show custom chords lol
        
    }
    return render(request, 'musicwebsite/index.html', context)

def chord_load(request):
    data = dict()
    
    chordList = list(Chord.objects.all())
    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))
    
    chords = dumps(dictList)
    
    data['chords'] = chords
    return JsonResponse(data)


def chord_create(request):
    #pdb.set_trace()
    data = dict()
    
    name = request.GET.get("name")
    base = request.GET.get("base")
    frets = request.GET.get("frets")
    fingers = request.GET.get("fingers")
    isCustom = request.GET.get("isCustom")
    
    Chord.objects.create(
                    name=name,
                    base=base,
                    frets=loads(frets), #must loads to make it back into JSON
                    fingers=loads(fingers), #must loads to make it back into JSON
                    isCustom=isCustom,
                    user= User.objects.first() #CURRENTLY GIVES CHORDS TO THE ADMIN INSTEAD OF LOGGED IN USER ############## ToDo
                )
    
    
    #generates the chord list html including the newly created chord, to be sent back to the javascript
    chords = Chord.objects.all()
    data['html_chord_list'] = render_to_string('musicwebsite/partial_chord_list.html', {
        'chords' : chords
    })
    
    
    
    
    return JsonResponse(data)
    

def chord_delete(request, id):
    #pdb.set_trace()
    data = dict()
    
    chord = Chord.objects.get(id=id)
    chord.delete()
    
    #copied code from create_chord view. This is to refresh the table
    chords = Chord.objects.all()
    data['html_chord_list'] = render_to_string('musicwebsite/partial_chord_list.html', {
        'chords' : chords
    })
    
    
    return JsonResponse(data)


def privacy_policy(request):
    return render(request, 'musicwebsite/privacy_policy.html')

def landing_page(request):
    return render(request, 'musicwebsite/landing_page.html')