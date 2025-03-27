from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' is actually email
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                next_url = request.POST.get('next', 'profile')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = UserLoginForm()
        
    context = {
        'form' : form
    }
    return render(request, 'users/registration.html', context)

def registration(request):
    return render(request, "users/registr.html")