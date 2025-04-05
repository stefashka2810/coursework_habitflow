from django.shortcuts import render, redirect
from .forms import HabitForm
from .models import Habit
from .models import Habit
from django.shortcuts import get_object_or_404, render
from datetime import timedelta


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

def habit_tracker_view(request, habit_id):
    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)

    start_date = habit.created_at.date()  
    end_date = habit.end_date

    dates_list = generate_date_points(start_date, end_date, habit.frequency)

    completions = habit.completions.filter(date__in=dates_list, completed=True)
    completed_dates = set(c.date for c in completions)

    context = {
        'habit': habit,
        'dates_list': dates_list,  
        'completed_dates': completed_dates,
    }
    return render(request, 'habits/habit_tracker.html', context)


def generate_date_points(start_date, end_date, frequency):

    result = []
    delta_map = {
        'daily': 1,
        'weekly': 7,
        'biweekly': 14,
        'monthly': 30,
        'semiannual': 180,
        'yearly': 365,
    }

    step = delta_map.get(habit_frequency_key(frequency), 1)
    
    current = start_date
    while current <= end_date:
        result.append(current)
        current += timedelta(days=step)
    
    return result


def habit_frequency_key(frequency):
    return frequency.lower()
