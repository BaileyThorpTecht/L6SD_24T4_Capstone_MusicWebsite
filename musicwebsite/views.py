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

import matplotlib.pyplot as plt
import numpy
from PIL import Image
import io
import base64   

# The views.
def index(request):

    chordList = list(Chord.objects.all())

    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))    
    
    dataJSON = dumps(dictList)
    
    context = {
        'data' : dataJSON,
        'chords' : Chord.objects.all(),
        
    }
    return render(request, 'musicwebsite/index.html', context)

def chord_list_render(req):
    chords = Chord.objects.all()


    return render_to_string('musicwebsite/partial_chord_list.html', {
        'chords' : chords,
    })





def chord_load(request):
    data = dict()
    
    chordList = list(Chord.objects.all())
    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))
    
    chords = dumps(dictList)
    
    data['chords'] = chords
    return JsonResponse(data)

def chord_draw(frets, base):
    base = int(base)
    try:
        frets = loads(frets)
    except:
        pass
    chord = []



    for i in range(0,6):
        chord.append([frets[i]+.5,i])

    fig, ax = plt.subplots(figsize=(5, 13))

    maxfret = max(base+4, max(frets))
    # Draw the fretboard
    ax.set_ylim(base, maxfret+1)
    ax.set_xlim(-1, 6)
    ax.set_yticks(numpy.arange(base, maxfret+1))
    ax.set_yticklabels([str(i) for i in range(base, maxfret+1)], fontsize=30)
    ax.set_xticks(numpy.arange(0, 6))
    ax.set_xticklabels(['', '', '', '', '', ''], fontsize=30)
    ax.xaxis.tick_top()

    # Draw the fret lines
    for i in range(0, 6):
        ax.axvline(i, color='black', lw=1)
    
    for i in range(base, maxfret+1):
        plt.axhline(i, color='black', lw=1, xmax=.85, xmin=.15)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.gca().invert_yaxis()

    # Plot custom fret positions
    labels = [item.get_text() for item in ax.get_xticklabels()]
    for fret, string in chord:
        print(fret)
        print(string)
        print(fret + string)
        if fret == -0.5:
            labels[string] = 'X'
        elif fret == 0.5:
            labels[string] = 'O'
        else:
            ax.plot(string, fret, 'o', color='red', markersize=30)

    ax.set_xticklabels(labels)
    print(labels)

    img = io.BytesIO()
    plt.savefig(img, format='PNG')
    img.seek(0)
    plt.close(fig)


    str_equivalent_image = str(base64.b64encode(img.getvalue()).decode())
    img_src = "data:image/png;base64," + str_equivalent_image

    return img_src

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
                    user= User.objects.first(), #CURRENTLY GIVES CHORDS TO THE ADMIN INSTEAD OF LOGGED IN USER ############## ToDo
                    image=chord_draw(frets,base)
                )
    
    
    #generates the chord list html including the newly created chord, to be sent back to the javascript
    data['html_chord_list'] = chord_list_render(request)

    
    
    
    
    return JsonResponse(data)
    

def chord_delete(request, id):
    #pdb.set_trace()
    data = dict()
    
    chord = Chord.objects.get(id=id)
    chord.delete()
    
    #copied code from create_chord view. This is to refresh the table
    chords = Chord.objects.all()
    data['html_chord_list'] = chord_list_render(request)
    
    
    return JsonResponse(data)


