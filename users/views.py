from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages, auth
from django.urls import reverse, NoReverseMatch
from django.http import HttpResponseRedirect
from .forms import UserLoginForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:main_after_registration'))
    else:
        form = UserLoginForm()
    return render(request, 'users/registration.html', {'form': form})

def registration(request):
    return render(request, "users/registr.html")