from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import News
from .models import Comment


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NewsForm(forms.ModelForm):

    class Meta:
        model = News

        fields = ['title', 'category', 'image', 'content']
        
        
class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = ['text']   