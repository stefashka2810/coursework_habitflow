from django.shortcuts import render, get_object_or_404, redirect
from .models import HabitNote
from habits.models import Habit
from .forms import HabitNoteForm


def all_notes_view(request):
    habits = Habit.objects.filter(user=request.user).prefetch_related('notes')
    if(habits): return render(request, 'habit_notes/all_notes.html', {'habits': habits})
    else: return render(request, 'habits/habitat_without_value.html')
 
def add_note(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        form = HabitNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.habit = habit
            note.save()
            return redirect('habit_notes:all_notes')
    else:
        form = HabitNoteForm()
    return render(request, 'habit_notes/note_form.html', {'form': form, 'habit': habit})

def delete_note(request, note_id):
    note = get_object_or_404(HabitNote, id=note_id)

    if request.method == 'POST':
        note.delete()
        return redirect('habit_notes:all_notes')
    
    # Обработка GET-запросов
    return redirect('habit_notes:all_notes') 
