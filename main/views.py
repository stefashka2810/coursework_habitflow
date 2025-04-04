from django.shortcuts import render

def index(request):
    return render(request, 'main/main_before_registration.html')

def about(request):
    return render(request, 'main/about.html')

def settings(request):
    return render(request, 'main/settings.html', {'user_obj': request.user})

def main_after_registration(request):
    return render(request, 'main/main_after_registration.html')