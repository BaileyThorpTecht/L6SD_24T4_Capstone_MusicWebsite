from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *

from django.core import serializers
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from json import dumps, loads

import pdb

from .forms import ChordForm



# The views.
def index(request):
    chords = Chord.objects.all()
    
    context = {
        'chords' : chords,
        'songs' : Song.objects.all(),
        'custom_chords' : chords.filter(isCustom=True),
        
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
        'chords' : chords,
        'custom_chords' : chords.filter(isCustom=True),
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
        'chords' : chords,
        'custom_chords' : chords.filter(isCustom=True),
    })
    
    
    return JsonResponse(data)







def song_list_render(req):
    selectedSongId = req.GET.get("song-id")
    selectedSong = Song.objects.filter(id=selectedSongId).first()
    if (selectedSong):
        selectedSongChords = selectedSong.songchord_set.all()
    else:
        selectedSongChords = SongChord.objects.none()
        
    renderContext = {
        'songs' : Song.objects.all(),
        'selected_song' : selectedSong,
        'selected_songchords' : selectedSongChords,
    }
    return render_to_string('musicwebsite/partial_song_list.html', renderContext)
    
    
    






def song_create(request):
    data = dict()
    #   pdb.set_trace()
    
    try:
        Song.objects.create(
            title = request.GET.get("song-name"),
            user = User.objects.first(),
        )
    except Exception as e:
        print(e)
    
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)

def song_load(request):
    data = dict()
    selectedSongId = request.GET.get("song-id")
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)

def song_update(request):
    data = dict()
    
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)

def song_delete(request):
    data = dict()
    
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)

