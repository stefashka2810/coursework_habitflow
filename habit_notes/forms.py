from django import forms
from .models import HabitNote

class HabitNoteForm(forms.ModelForm):
    class Meta:
        model = HabitNote
        fields = ['date', 'note', 'photo', 'mood']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'mood': forms.Select(),
            'note': forms.Textarea(attrs={'rows': 4}),
        }
