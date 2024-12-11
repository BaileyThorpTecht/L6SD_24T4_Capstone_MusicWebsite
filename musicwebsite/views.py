from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from .models import *

from django.core import serializers
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from json import dumps, loads

import pdb

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy
from PIL import Image
import io
import base64
from .forms import ChordForm   

def getBaseFromFrets(frets):
    base = 1
    #the base is the lowest non- 0, non- -1 fret
    positiveFrets = [fret for fret in frets if fret > 0] #exclude 0 and -1
    
    if positiveFrets:
        base = min(positiveFrets)
    else:
        base = 1
        
    for i in range(6):
        if frets[i] > 0:
            frets[i] = frets[i] - base + 1
            #change frets to account for the base
    
    return base, frets



# The views.
def index(request):

    chordList = list(Chord.objects.all())

    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))    
    
    dataJSON = dumps(dictList)
    
    chords = Chord.objects.all()
    user = request.user
    userId = user.id
    
    context = {
        'chords' : chords,
        'songs' : Song.objects.filter(user=userId),
        'custom_chords' : chords.filter(isCustom=True, user=userId),
        'user' : user
        
        
    }
    return render(request, 'musicwebsite/index.html', context)

#(not a view) generates the html to be put in the custom chord list section of the page. Is used at the end of every chord_* view
def chord_list_render(req): 
    chords = Chord.objects.all()
    user = req.user
    userId = user.id


    return render_to_string('musicwebsite/partial_chord_list.html', {
        'chords' : chords,
        'custom_chords' : chords.filter(isCustom=True, user=userId),
        'user' : user
        
    })

#gets chords from database to be put into a javascript variable 
def chord_read(request):
    data = dict()
   
    chordList = list(Chord.objects.all())
    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))
   
    chords = dumps(dictList)
   
    data['chords'] = chords
    return JsonResponse(data)


#just reloads the custom chord section. Is used when adding a chord which doesnt yet exist to a song, so a new one is created and the list needs to be reloaded
def chord_load(request):
    data = dict()
    
    #generates the chord list html including any changes, to be sent back to the javascript
    chords = Chord.objects.all()
    data['html_chord_list'] = chord_list_render(request)

    return JsonResponse(data)

#(not a view) returns an image representing a chord. Uses frets and base of that chord as input
def chord_draw(frets, base):
    base = int(base)
    try:
        frets = loads(frets)
    except:
        pass

    # Creates a list with nested lists for matplotlib to read fret positions
    chord = []
    for i in range(0,6):
        chord.append([frets[i]+.5,i]) 

    fig, ax = plt.subplots(figsize=(5, 13))
    maxfret = max(base+4, max(frets))

    # Draw the fretboard
    ax.set_ylim(base, maxfret+1)
    ax.set_xlim(-1, 6)
    ax.set_yticks(numpy.arange(base, maxfret+1))
    ylabel = [str('') for i in range(base, maxfret+1)] # Sets empty labels to prevent function from breaking when changing a value
    ylabel[0] = "\n" + str(base) + "fr."
    ax.set_yticklabels(ylabel, fontsize=30)
    ax.set_xticks(numpy.arange(0, 6))
    ax.set_xticklabels(['', '', '', '', '', ''], fontsize=30) # Sets empty labels to prevent function from breaking when changing a value
    ax.xaxis.tick_top() # Moves X axis labels to top of graph

    # Draw the fret lines and strings
    for i in range(0, 6):
        ax.axvline(i, color='black', lw=3)
    for i in range(base, maxfret+1):
        plt.axhline(i, color='black', lw=3, xmax=.85, xmin=.15)

    # Makes graph borders invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Flips graph vertically to match actual chord diagrams
    plt.gca().invert_yaxis()


    # Plot custom fret positions and set X or O labels for open or inactive strings
    labels = [item.get_text() for item in ax.get_xticklabels()]
    for fret, string in chord:
        if fret == -0.5:
            labels[string] = 'X'
        elif fret == 0.5:
            labels[string] = 'O'
        else:
            ax.plot(string, fret+base-1, 'o', color='black', markersize=30)
    ax.set_xticklabels(labels)

    # Set graph size ratio
    fig.set_size_inches(6,4.4)
    
    # Saves graph as PNG into memory with an equivelant string to save into the Chord object.
    img = io.BytesIO()
    plt.savefig(img, format='PNG', bbox_inches="tight")
    img.seek(0)
    plt.close(fig)
    str_equivalent_image = str(base64.b64encode(img.getvalue()).decode())
    img_src = "data:image/png;base64," + str_equivalent_image

    return img_src


#creates a chord in database using the fretboard and name input from the page, then reloads custom chord list. Used from the 'save chord' button under the chord list
def chord_create(request):
    data = dict()

    name = request.GET.get("name")
    base = request.GET.get("base")
    frets = loads(request.GET.get("frets"))
    fingers = loads(request.GET.get("fingers"))
    isCustom = request.GET.get("isCustom")
    user = request.user
    
    if (user.is_authenticated):
    
        base, frets = getBaseFromFrets(frets)
        
        
        #check for existing chord
        chosenFrets = frets

        chords = Chord.objects.filter(isCustom=False)

        matched = False
        matchedChord = False
        for chord in chords:
            checkingFrets = chord.frets
        
            for i in range(6):          
                if ((chosenFrets[i] == checkingFrets[i] + chord.base - 1) or (checkingFrets[i] == chosenFrets[i] == -1)):
                    if (i == 5):
                        matched = True
                        break
                else:
                    break
            
            if (matched):
                matchedChord = chord
                break
        
        if (matchedChord):
            name = matchedChord.name
        
        
        
        
        
        Chord.objects.create(
                        name=name,
                        base=base,
                        frets=frets,
                        fingers=fingers, 
                        isCustom=isCustom,
                        user=user,
                        image=chord_draw(frets,base)
                )
    
    
    #generates the chord list html including the newly created chord, to be sent back to the javascript
    data['html_chord_list'] = chord_list_render(request)

    return JsonResponse(data)
    

#deletes a chord, then reloads the chord list view. Used from the'DELETE' button from a chord in the custom chord list
def chord_delete(request, id):
    #pdb.set_trace()
    data = dict()
    
    chord = Chord.objects.get(id=id)
    chord.delete()
    
    data['html_chord_list'] = chord_list_render(request)
    
    return JsonResponse(data)

#(not a view) generates the html to be put in the song list section. Is used at the end of every song_* view
def song_list_render(req):
    selectedSongId = req.GET.get("song-id")
    
    user = req.user
    userId = user.id
    songs = Song.objects.all()
    availableSongs = songs.filter(user=userId)
    
    selectedSong = availableSongs.filter(id=selectedSongId).first()
    if (selectedSong):
        selectedSongChords = selectedSong.songchord_set.all()
    else:
        selectedSongChords = SongChord.objects.none()
       
    renderContext = {
        'songs' : availableSongs,
        'selected_song' : selectedSong,
        'selected_songchords' : selectedSongChords,
        'user' : user
    }
    return render_to_string('musicwebsite/partial_song_list.html', renderContext)
   
   
 
#creates a song, then reloads the song list. Used from the 'create song' button in the songs list
def song_create(request):
    data = dict()
    user = request.user
    
    if (user.is_authenticated):
   
        try:
            Song.objects.create(
                title = request.GET.get("song-name"),
                user = user
            )
        except Exception as e:
            print(e)
   
   
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)
 
 
#just reloads the song list. Used when selecting a new song
def song_load(request):
    data = dict()
   
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)
 
 
#adds a songchord to a song, then reloads the song list. Creates a new custom chord if it doesnt already exist. Used on the 'add chord' button in a song
def song_update(request):
    data = dict()
    
    user = request.user
    
    if (user.is_authenticated):
        chosenFrets = loads(request.GET.get("selected-frets"))

        chords = Chord.objects.filter(Q(user=user.id) | Q(isCustom=False))

        #check if a chord with those frets already exists
        matched = False
        matchedChord = False
        for chord in chords:
            checkingFrets = chord.frets
        
            for i in range(6):          
                if ((chosenFrets[i] == checkingFrets[i] + chord.base - 1) or (checkingFrets[i] == chosenFrets[i] == -1)):
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
            
            base, chosenFrets = getBaseFromFrets(chosenFrets)
            
            matchedChord = Chord.objects.create(
                name=request.GET.get("default-name"),
                base=base,
                frets=chosenFrets,
                fingers=[1,2,3,4,0,0],
                isCustom=True,
                user=user,
                image=chord_draw(chosenFrets,base)
        
            )
        #create songchord in song
        SongChord.objects.create(
            song=Song.objects.get(id=request.GET.get("song-id")),
            chord=matchedChord,
            position=1,
            length=1,
        )

    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)


#creates a songchord, then reloads the song list. Used from the add chord to current song '+' button in the chord list
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
 
#deletes song then reloads the song list. Used from the 'delete song' button in the song section
def song_delete(request):
    data = dict()
   
    deleteId = request.GET.get("delete-id")
    Song.objects.filter(id=deleteId).delete()
   
    print(request.GET)
   
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)
 
#deletes a songchord then reloads the song list. Used from the 'DELETE' button on a songchord in the song section
def song_remove(request, id):
    data = dict()
   
    SongChord.objects.filter(id=id).delete()
       
    data['html_song_list'] = song_list_render(request)  
    return JsonResponse(data)
 
 
#plays the current song.
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

def landing_page(request):
    return render(request, 'musicwebsite/landing_page.html')