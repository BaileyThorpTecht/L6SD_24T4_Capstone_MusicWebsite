from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord
from musicwebsite.forms import ChordVerificationForm
from django.core import serializers
from django.forms.models import model_to_dict

from json import dumps
from json import dump


# The views.
def index(request):
    
    chordList = list(Chord.objects.all())
    #frets = [chord.frets for chord in chords]
    
    dictList = []
    for x in chordList:
        dictList.append(model_to_dict(x))    
    
    dataJSON = dumps(dictList)
    
    #with open('data.json', 'w') as f:
    #    dump(dataJSON, f)
    
    context = {
        'data' : dataJSON,
    }
    return render(request, 'musicwebsite/index.html', context)




