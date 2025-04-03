# habits/urls.py
from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('create/', views.create_habit, name='create_habit'),
    path('tracker/', views.habit_tracker, name='habit_tracker'),
    # path('', views.habit_list, name='habit_list'),
]
