from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from gems.models import Category, Gem, Comment
from gems.forms import GemForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
    
    #Render!
    return render(request,'gems/sign_up.html',
    {'user_form':user_form,'profile_form':profile_form,'registered':registered})

def log_in(request):
    if request.method == 'POST':
        # Gather user information from login form
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Use django to see if username/password combination is valid
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active?
            if user.is_active:
                # If active, log them in
                login(request,user)
                # Send loggined in user back to homepage
                return HttpResponseRedirect(reverse('index'))

            else:
                # Can't log in without an active account!
                return HttpResponse("Your Glasgow Gems Account is disabled")
        
        else:
            # Bad login details provided
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    
    else:
        # Render the template
        return render(request,'gems/login.html',{})

# Login Required Views - Restricted Access

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
	
def search_results(request):
	search_results = []
	query = request.GET.get("q")
	if query:
		search_results = Gem.objects.filter(Q(name__icontains=query))
	return render(request, 'gems/search_results.html', {'search_results': search_results, 'search' : query})