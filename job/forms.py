from django import forms
from django.forms import TextInput
from .models import job
from django.forms import ModelForm
class SearchForm(forms.Form):
    search = forms.CharField(required=True)

class PostCreateForm(ModelForm):
    class Meta:
        model=job
        fields=['job_title','location','discription','company_name','company_logo','website_url']
   
