from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):

    name = forms.CharField()
    description = forms.CharField()
    category = forms.CharField()
    frequency = forms.CharField()
    end_date = forms.CharField()
    
    class Meta:
        model = Habit
        fields = ['name', 'description', 'category', 'frequency', 'end_date']

