from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Chord
from musicwebsite.forms import ChordVerificationForm


# The views.
def index(request):
    context = {
        "context_name" : "context data"
    }
    return render(request, 'musicwebsite/index.html', context)




