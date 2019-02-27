from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context_dict = {'boldmessage':"Glasgow Gems"}
    return render(request,'gems/index.html',context=context_dict)

def about(request):
    context_dict = {'boldmessage':"This is the about page!"}
    return render(request,'gems/about.html',context=context_dict)
    