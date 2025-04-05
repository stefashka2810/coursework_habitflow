from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegisterForm
from habits.models import Habit

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
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    return render(request, "users/registr.html", {'form': form})


def profile(request):
    habits = Habit.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'habits': habits
    }
    return render(request, "users/profile.html", context)

def logout(request):
    auth.logout(request)
    return redirect('main:index')

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        auth.logout(request)           
        user.delete()            
        return redirect('main:index')  
    return redirect('main:settings')  
