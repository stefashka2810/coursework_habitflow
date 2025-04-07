from django.urls import path
from . import views

app_name = 'habit_notes'

urlpatterns = [
    path('', views.all_notes_view, name='all_notes'),
    path('habit/<int:habit_id>/notes/add/', views.add_note, name='add_note'),
]
