from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HabitForm

@login_required
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
    
    return render(request, 'habits/create_habit.html', {'form': form})
