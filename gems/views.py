from django.shortcuts import render, redirect
from django.http import HttpResponse
from gems.models import Category, Gem, Comment
from gems.forms import GemForm

def index(request):
    category_list = Category.objects.all()
    most_liked_gems = Gem.objects.order_by('-likes')[:10]
    most_recent_gems = Gem.objects.order_by('-added_on')[:10]
    context_dict = {'categories': category_list, 'most_liked_gems': most_liked_gems,
                    'most_recent_gems': most_recent_gems}
    return render(request,'gems/index.html', context_dict)

def contact_us(request):
    context_dict = {'boldmessage':"This is the contact us page!"}
    return render(request,'gems/contact_us.html', context_dict)
    
def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        gems = Gem.objects.filter(category=category)
        context_dict['gems'] = gems
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['gems'] = None
    return render(request, 'gems/category.html', context_dict)

def show_gem(request, category_name_slug, gem_name_slug):
    context_dict = {}
    try:
        gem = Gem.objects.get(slug=gem_name_slug)
        comments = Comment.objects.filter(gem=gem)
        context_dict['gem'] = gem
        context_dict['comments'] = comments
    except Gem.DoesNotExist:
        context_dict['comments'] = None
        context_dict['gem'] = None
    return render(request, 'gems/gem.html', context_dict)

def add_gem(request):
    form = GemForm()
    
    if request.method == 'POST':
        form = GemForm(request.POST, request.FILES) # FILES needed for image
        if form.is_valid():
            gem = form.save(commit=True)
            #===================================================================
            # NONE OF THIS IS NEEDED, DONE AUTOMATICALLY FROM THE FORM,
            # ONLY NEEDED IF NEED TO SET SOME FIELDS OURSELVES, REMEMBER!
            # gem.name = name
            # gem.category = category
            # gem.address = address
            # gem.image = form.cleaned_data['image']
            # gem.image_source = image_source
            # gem.description = description
            # gem.likes = likes
            # gem.reported = reported
            # gem.added_on = added_on
            # gem.save()
            #===================================================================
            return redirect('show_gem', gem.category.slug, gem.slug)
            # do not use! only shows the view, does not update URL, above does
            #return show_gem(request, gem.category.slug, gem.slug)
        else:
            print(form.errors)
    
    context_dict = {'form':form}
    return render(request,'gems/add_gem.html', context_dict)
