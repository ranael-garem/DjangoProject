from django import forms
from django.contrib.auth.models import User
from main.models import Book


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class BookEditForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['name', 'author']
