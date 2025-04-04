from django.shortcuts import render, redirect
from .forms import HabitForm
from .models import Habit
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Habit
from django.utils.dateparse import parse_date


def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user  
            habit.save()
            return redirect('habits:habit_list')  
    else:
        form = HabitForm()
    
    return render(request, 'habits/add_habitat.html', {'form': form})

def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    if(habits): return render(request, 'habits/list_habitats.html', {'habits': habits})
    else: return render(request, 'habits/habitat_without_value.html')