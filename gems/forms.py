from django import forms
from gems.models import Gem, Category, UserProfile
from django.contrib.auth.models import User

class GemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), help_text="Category:")
    
    name = forms.CharField(max_length=99, help_text="Name:")
    address = forms.CharField(max_length=99, help_text="Address:")
    description = forms.CharField(max_length=200, help_text="Description:", widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}))
    
    image = forms.ImageField(help_text="Upload image:")
    image_source = forms.CharField(max_length=99, help_text="Image source:")
    
    # populated automatically from the map marker
    latitude = forms.DecimalField(widget=forms.HiddenInput())
    longitude = forms.DecimalField(widget=forms.HiddenInput())
    
    # fields that users do not populate
    # initial or required parameter needed, otherwise form.is_valid() returns False
    likes = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    reported = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    
    #added_by changed in add_gem view after the form is submitted
    added_on = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Gem
        # using fields specifies the display order
        fields = ('name', 'address', 'category', 'image', 'image_source',
                  'description', 'latitude', 'longitude')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_image',)
