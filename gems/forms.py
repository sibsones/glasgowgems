from django import forms
from gems.models import Gem, Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter category name: ")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class GemForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text="Please enter title of Gem: ")
    url = forms.URLField(max_length=200,help_text="Please enter url of Gem: ") #Not sure if we'll use this - Luis
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    def clean(self):
        #Adding http to url's of Gems - Luis
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        model = Gem
        #Can exclude certain fields - Luis
        exclude = ('category',)
        #Or specify fields to include, .i.e. - Luis
        #Fields = ('title','url','views')