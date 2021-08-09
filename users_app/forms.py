from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import Users
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import authenticate, password_validation


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('First name')}),
                            label=("First name"), required=False)

    image = forms.ImageField(required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('Last name')}),
                            label=("Last name"), required=False)

    patronymic = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('Patronymic')}))

    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': ('Username')}),
                            label=("Username"), required=True)

    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Phone')}),
                       label=("Phone number"), required=False)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('Password')}), label=("Password"))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('Password')}), label=("Password"))

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'patronymic', 'phone_number', 'username', 'password1', 'password2']


class LogForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ('username')}),
                             label=("Username"), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ('Password')}), label=("Password"), required=True)

    class Meta:
        model = Users
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password,):

            raise forms.ValidationError("Invalid login")

