from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    context = {
        "context_name" : "context data"
    }
    return render(request, 'musicwebsite/index.html', context)


