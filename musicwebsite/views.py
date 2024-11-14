from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord

from django.core import serializers
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from json import dumps
from json import dump

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
    }
    return render(request, 'musicwebsite/index.html', context)


def chord_create(request):
    pdb.set_trace()
    data = dict()
    print(request.method)
    print(request.GET.get("name"))
    if request.method == 'POST':
        form = ChordForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            data['form_is_valid'] = True            
        else:            
            data['form_is_valid'] = False
            
    else:        
        form = ChordForm()
        

    context = {'form': form}
    
    data['html_form'] = render_to_string('partial_chord_create.html',
        context,
        request=request
    )
    
    return JsonResponse(data)
    




