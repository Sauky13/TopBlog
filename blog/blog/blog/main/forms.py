from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    age = forms.IntegerField(label='Возраст', max_value=100)
    avatar = forms.ImageField(label='Фото профиля', required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'age', 'avatar', 'username', 'password1', 'password2', 'email')


class ChangeUserInfoForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    age = forms.IntegerField(label='Возраст', max_value=100, required=False)
    avatar = forms.ImageField(label='Фото профиля', required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'age', 'avatar')
