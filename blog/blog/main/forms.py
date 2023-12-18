from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Comment


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

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('delete_avatar'):
            user.avatar.delete(save=False)

        if commit:
            user.save()

        return user


class CreatePost(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Что у вас нового?'}),
        label=''
    )
    image = forms.ImageField(label='', required=False)

    class Meta:
        model = Post
        fields = ('text', 'image')


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Добавьте комментарий...'}),
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content', 'image']
