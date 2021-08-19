from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Users
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import authenticate
from oil_grants.models import EdProgram


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}),
                               label="Username", required=True)

    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'}),
                                 label="Имя*", required=True)

    # image = forms.ImageField(required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'form-control'}),
                                label="Фамилия*", required=True)

    patronymic = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Отчество', 'class': 'form-control'}),
                                 label="Отчество", required=False)

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email адрес', 'class': 'form-control'}),
                             label="Email адрес*", required=True)

    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'form-control'}),
                                    label="Телефон*", required=True)

    birthplace = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Место рождения', 'class': 'form-control'}),
                                 label="Место рождения", required=False)

    social_status = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Социальный статус', 'class': 'form-control'}),
                                    label="Социальный статус", required=False)

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'patronymic', 'birthplace', 'social_status', 'email', 'phone_number',
                  'username']


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
                                 label="Имя*", required=True)

    # image = forms.ImageField(required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                                label="Фамилия*", required=True)

    patronymic = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Отчество'}),
                                 label="Отчество", required=False)

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email адрес'}),
                             label="Email адрес*", required=True)

    uin = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ИИН'}),
                          label="ИИН*", required=True)

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}),
                               label="Логин*", required=True)

    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Телефон'}),
                                    label="Телефон*", required=True)

    birthplace = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Место рождения'}),
                                 label="Место рождения", required=False)

    social_status = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Социальный статус'}),
                                    label="Социальный статус", required=False)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="Пароль")

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}),
                                label="Подтверждение пароля")

    edProgram = forms.ModelChoiceField(widget=forms.Select(attrs={'placeholder': 'Специальность', 'style': 'width: 300px; height: 45px;'}),
                                       queryset=EdProgram.objects.all(),  label="Специальность")

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'patronymic', 'uin', 'birthplace', 'social_status', 'email', 'phone_number',
                  'edProgram', 'username', 'password1', 'password2']


class LogForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'логин'}),
                               label="Логин", required=True)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'пароль'}), label="Пароль",
                               required=True)

    class Meta:
        model = Users
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Invalid login")


class PasswordUpdateForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'старый пароль', 'class': 'form-control'}),
                                   label="Старый пароль",
                                   required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'новый пароль', 'class': 'form-control'}),
                                    label="Новый пароль",
                                    required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'подтвердите пароль', 'class': 'form-control'}),
                                    label="Подтвердите пароль",
                                    required=True)

    class Meta:
        model = Users
        fields = ['old_password', 'new_password1', 'new_password2']