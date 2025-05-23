from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name= 'index'),
    path('about/', views.about, name= 'about'),
    path('about_us/', views.about_us, name= 'about_us'),
    path('settings/', views.settings, name= 'settings'),
    path('main-after-registration/', views.main_after_registration, name='main_after_registration'),
]
