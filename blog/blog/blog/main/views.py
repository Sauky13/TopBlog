from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserForm, ChangeUserInfoForm
from .models import CustomUser


def index(request):
    return render(request, 'main/index.html')


class LoginViewUser(LoginView):
    template_name = 'main/login.html'


def logout_view(request):
    logout(request)
    return render(request, 'main/logout.html')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class UserRegister(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main:register_done')


class RegisterDone(TemplateView):
    template_name = 'registration/register_done.html'


def edit_user(request):
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:profile')
    else:
        form = ChangeUserInfoForm(instance=request.user)

    return render(request, 'main/change_user_info.html', {'form': form})
