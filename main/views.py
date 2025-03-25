from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'main/main_before_registration.html')

def about(request):
    return HttpResponse('About page')