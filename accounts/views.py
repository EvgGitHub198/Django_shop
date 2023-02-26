from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            if form.is_valid():
                form.save()
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect('login')
        else:
            messages.error(request, 'Неправильная проверка reCAPTCHA. Пожалуйста, попробуйте еще раз.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'site_key': settings.RECAPTCHA_SITE_KEY, 'messages': messages.get_messages(request)})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')
