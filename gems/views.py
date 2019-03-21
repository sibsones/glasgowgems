from django.shortcuts import render, redirect
from django.http import HttpResponse
from gems.models import Category, Gem, Comment
from gems.forms import GemForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def index(request):
    category_list = Category.objects.all()
    most_liked_gems = Gem.objects.order_by('-likes')[:10]
    most_recent_gems = Gem.objects.order_by('-added_on')[:10]
    context_dict = {'categories': category_list, 'most_liked_gems': most_liked_gems,
                    'most_recent_gems': most_recent_gems}
    return render(request,'gems/index.html', context_dict)

def contact_us(request):
    category_list = Category.objects.all()
    info = "Please send us an email to adminteam@glasgowgems.com " \
           "and we will be back in touch as soon as possible."
    context_dict = {'categories': category_list,'boldmessage': info}
    return render(request, 'gems/contact_us.html', context_dict)
    
def show_category(request, category_name_slug):
    context_dict = {}
    category_list = Category.objects.all()
    context_dict['categories'] = category_list
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
    category_list = Category.objects.all()
    context_dict['categories'] = category_list
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
    if request.user.is_authenticated:
        form = GemForm()
        
        if request.method == 'POST':
            form = GemForm(request.POST, request.FILES) # FILES needed for image
            if form.is_valid():
                gem = form.save(commit=False)
                gem.added_by = request.user # logged in user
                gem.save()
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
        
        category_list = Category.objects.all()
        context_dict = {'form':form, 'categories': category_list}
        return render(request, 'gems/add_gem.html', context_dict)
    else:
        return redirect('login')

def search_results(request):
    search_results = []
    query = request.GET.get("q")
    if query:
        search_results = Gem.objects.filter(Q(name__icontains=query)).order_by('name')
    category_list = Category.objects.all()
    context_dict = {'search_results': search_results, 'search': query,
                    'categories': category_list}
    return render(request, 'gems/search_results.html', context_dict)

# User related views

def sign_up(request):
    # Was the registration successful?
    registered = False

    if request.method == 'POST':
        # Grab information
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the 2 forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save!
            user = user_form.save()
            # Hash and Save the password
            user.set_password(user.password)
            user.save()

            # Profile Form
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did user provide profile image?
            if 'profile_image' in request.FILES:
                # Retrieve it
                profile.picture = request.FILES['picture']
            # Save profile!
            profile.save()
            # Indicate successful registration
            registered = True
        else:
            # If form invalid, mistakes etc.... print to terminal
            print(user_form.errors,profile_form.errors)
    else:
        # Blank forms ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    category_list = Category.objects.all()
    context_dict = {'user_form':user_form, 'profile_form':profile_form,
                    'registered':registered, 'categories': category_list}
    return render(request, 'gems/sign_up.html', context_dict)

def log_in(request):
    if request.method == 'POST':
        # Gather user information from login form
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Use django to see if username/password combination is valid
        user = authenticate(username=username, password=password)

        if user:
            #===================================================================
            # Code in these blocks is useless, in Django 1.10+ authenticate
            # checks user.is_active automatically and if not returns None, i.e.
            # else in the block below can never be reached
            #===================================================================
            
            #===================================================================
            # # Is the account active?
            # if user.is_active:
            #===================================================================
            
            # Active, log them in
            login(request,user)
            # Send logged in user back to index
            return redirect('index')

            #===================================================================
            # else:
            #     # Can't log in without an active account!
            #     messages.info(request, 'Your account is disabled. Contact us for more info.')
            #     return redirect('login')
            #===================================================================
        
        else:
            # Bad login details provided
            messages.error(request, 'Username or password incorrect. Try again.')
            return redirect('login')
    
    else:
        # Render the login template
        category_list = Category.objects.all()
        return render(request, 'gems/login.html', {'categories': category_list})

def like_gem(request):
    gem_id = None
    if request.method == 'GET':
        gem_id = request.GET['gem_id']
    likes = 0
    if gem_id:
        gem = Gem.objects.get(id=int(gem_id))
        if gem:
            likes = gem.likes + 1
            gem.likes = likes
            gem.save()
    return HttpResponse(likes)
	
@csrf_exempt
def create_comment(request):
    gem_id = None
    if request.method == 'POST':
        gem_id = request.POST['gem_id']
        if gem_id:
            gem = Gem.objects.get(id=int(gem_id))
            comment_text = request.POST.get('comment_text')
            comment = Comment.objects.create(gem = gem, text=comment_text, added_by = request.user)
            comment.save() 
    return redirect('show_gem',gem.category.slug,gem.slug)
    
def report(request):
    gem_id = None
    if request.method == 'GET':
        gem_id = request.GET['gem_id']
    if gem_id:
        gem = Gem.objects.get(id=int(gem_id))
        if gem:
            gem.reported = True
            gem.save()
    return HttpResponse(likes)   
    
@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
	
def profile(request):
    if request.user.is_authenticated:
        ### TO BE CHANGED WHEN PROFILE IS IMPLEMENTED
        category_list = Category.objects.all()
        return render(request, 'gems/contact_us.html', {'categories': category_list})
    else:
        return redirect('login')
