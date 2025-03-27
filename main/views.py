from django.shortcuts import render

def index(request):
    return render(request, 'main/main_before_registration.html')

def about(request):
    return render(request, 'main/about.html')