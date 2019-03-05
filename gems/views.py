from django.shortcuts import render
from django.http import HttpResponse
from gems.models import Category
from gems.models import Gem
from gems.forms import CategoryForm
from gems.forms import GemForm

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

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

        else:
            print(form.errors)

    return render(request,'gems/add_category.html',{'form':form})

def add_gem(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = GemForm()
    
    if request.method == 'POST':
        form = GemForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request,'gems/add_gem.html',context_dict)