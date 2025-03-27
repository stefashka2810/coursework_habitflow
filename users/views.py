from django.shortcuts import render

def login(request):
    return render(request, 'users/registration.html')

def registration(request):
    return render(request, "users/registr.html")