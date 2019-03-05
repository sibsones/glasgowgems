from django.shortcuts import render
from django.http import HttpResponse
from gems.models import Category
from gems.models import Gem

# Create your views here.

def index(request):
    category_list = Category.objects.all()
    gem_list = Gem.objects.order_by('-likes')[:10]
    context_dict = {'categories': category_list, 'gems': gem_list}
    return render(request,'gems/index.html',context_dict)

def about(request):
    context_dict = {'boldmessage':"This is the about page!"}
    return render(request,'gems/about.html',context=context_dict)
    
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        gems = Gem.objects.filter(category=category)
        context_dict['gems'] = gems
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['Gem'] = None
    return render(request, 'gems/category.html', context_dict)