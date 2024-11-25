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



# The views.
def index(request):
    chords = Chord.objects.all()
    
    context = {
        'chords' : chords,
        'songs' : Song.objects.all(),
        'custom_chords' : chords.filter(isCustom=True),
        
    }
    return render(request, 'musicwebsite/index.html', context)

def chord_read(request):
    data = dict()
    
    chordList = list(Chord.objects.all())
    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))
    
    chords = dumps(dictList)
    
    data['chords'] = chords
    return JsonResponse(data)


def chord_load(request):
    data = dict()
    
    #generates the chord list html including any changes, to be sent back to the javascript
    chords = Chord.objects.all()
    data['html_chord_list'] = render_to_string('musicwebsite/partial_chord_list.html', {
        'chords' : chords,
        'custom_chords' : chords.filter(isCustom=True),
    })
    
    
    
    
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
    
    
    #copied code from load_chord view. This is to refresh the table
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
    
    #copied code from load_chord view. This is to refresh the table
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
    print(request.GET)
    
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
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)

def song_update(request):
    data = dict()
    
    chosenFrets = loads(request.GET.get("selected-frets"))
    chords = Chord.objects.all()
    
    #check if a chord with those frets exists
    matched = False
    matchedChord = False
    for chord in chords:
        checkingFrets = chord.frets
        
        for i in range(6):          
            if ((checkingFrets[i] == chosenFrets[i] + chord.base - 1) or (checkingFrets[i] == chosenFrets[i] == -1)):
                if (i == 5):
                    matched = True
                    break
            else:
                break
            
        if (matched):
            matchedChord = chord
            break

    #if a chord was not found, make one
    if not matchedChord:
        matchedChord = Chord.objects.create(
            name=request.GET.get("default-name"),
            base=1,
            frets=chosenFrets,
            fingers=[1,2,3,4,0,0],
            isCustom=True,
            user= User.objects.first(), #CURRENTLY GIVES CHORDS TO THE ADMIN INSTEAD OF LOGGED IN USER ############## ToDo
    
        )
    
    SongChord.objects.create(
        song=Song.objects.get(id=request.GET.get("song-id")),
        chord=matchedChord,
        position=1,
        length=1,
    )
    
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)

def song_update_from_chords(request, id):
    data = dict()
    
    SongChord.objects.create(
        song=Song.objects.get(id=request.GET.get("song-id")),
        chord=Chord.objects.get(id=id),
        position=1,
        length=1,
    )
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)


def song_delete(request):
    data = dict()
    
    deleteId = request.GET.get("delete-id")
    Song.objects.filter(id=deleteId).delete()
    
    print(request.GET)
    
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)

def song_remove(request, id):
    data = dict()
    
    SongChord.objects.filter(id=id).delete()
        
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)



def song_play(request):
    data = dict()
    #pdb.set_trace()
    
    data['success'] = False
    
    songId = request.GET.get("song-id")
    songs = Song.objects.filter(id=songId)
    if songs.count() > 0:
        song = songs[0]
        songChords = song.songchord_set.all()
        
        fretsList = list()
        chordList = list()
        for songChord in songChords:
            fretsList.append(songChord.chord.frets)
            chordList.append(model_to_dict(songChord.chord))
            
        data['chords'] = dumps(chordList)
        data['success'] = True
        
    return JsonResponse(data)
    
    
    


