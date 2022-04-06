from .models import Post,Comments,Profile
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=300, help_text='Enter a valid email address')
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput,required=True)

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
        ]

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=300, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email',
            'password', 
        ]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'image',
            'caption'
        ]

class CommentsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Type comment...'

    class Meta:
        model = Comments
        fields = ('comment',)

