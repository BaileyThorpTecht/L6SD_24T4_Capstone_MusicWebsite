from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord

from django.core import serializers
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from json import dumps
from json import dump

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
    }
    return render(request, 'musicwebsite/index.html', context)


def chord_create(request):
    form = ChordForm()
    context = {'form': form}
    html_form = render_to_string('partial_chord_create.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})
    




