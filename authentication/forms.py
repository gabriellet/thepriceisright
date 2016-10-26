# authentication/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(AuthenticationForm):
	username = forms.CharField(label="Username", max_length=30, 
		widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
	password = forms.CharField(label="Password", max_length=30, 
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')