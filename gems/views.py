from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Glasgow Gems index! <br/> <a href='/about/'>About</a>.")

def about(request):
    return HttpResponse("Glasgow Gems About! <br/> <a href='/'>Index</a>.")