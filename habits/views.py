from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HabitForm


def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user  
            habit.save()
            return redirect('habits:habit_tracker')  
    else:
        form = HabitForm()
    
    return render(request, 'habits/add_habitat.html', {'form': form})

def habit_tracker(request):
    return render(request, 'habits/habit_tracker.html')