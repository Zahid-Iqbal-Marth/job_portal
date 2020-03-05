from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer,Resume,Experience,Education
from django.forms import TextInput,EmailInput,PasswordInput

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
class ProfileUpdateForm(forms.ModelForm):
   class Meta:
        model = Customer
        fields = ('country','state','city','zip_code','phone')

class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True,widget=TextInput)
    first_name = forms.CharField(required=True,widget=TextInput)
    last_name = forms.CharField(required=True,widget=TextInput)
    email = forms.EmailField(required=True, widget=EmailInput)
    password=forms.CharField(required=True, widget=PasswordInput)
    TYPE = [
        ('EM','Employer'),
        ('CN', 'Candidate'),
        ('NN', 'None'),
    ]
    Type = forms.ChoiceField(
    choices=TYPE,
    )

class AddResumeForm(forms.Form):

    profession_title = forms.CharField(required=True)
    location = forms.CharField(required=True)
    photo = forms.ImageField()
    resume_content = forms.CharField(required=True)

    school_name = forms.CharField(required=True)
    qualifications = forms.CharField(required=True)
    Ed_start_end_date = forms.CharField(required=True)
    Ed_notes = forms.CharField()

    employer = forms.CharField(required=True)
    job_title = forms.CharField(required=True)
    Ex_start_end_date = forms.CharField(required=True)
    Ex_notes = forms.CharField()




class UpdateResume(forms.ModelForm):
    class Meta:
        model = Resume
        exclude=['name']

class UpdateEducation(forms.ModelForm):
    class Meta:
        model = Education
        exclude=['name']

class UpdateExprience(forms.ModelForm):
    class Meta:
        model = Experience
        exclude=['name']