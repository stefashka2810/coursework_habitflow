from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages, auth
from django.urls import reverse, NoReverseMatch
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:main_after_registration'))
    else:
        form = UserLoginForm()
    return render(request, 'users/registration.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:main_after_registration'))
    else:
        form = UserRegisterForm()
    return render(request, "users/registr.html", {'form': form})