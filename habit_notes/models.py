from django.db import models
from habits.models import Habit
from django.utils import timezone

class HabitNote(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('neutral', '😐 Neutral'),
        ('sad', '😞 Sad'),
        ('angry', '😠 Angry'),
        ('tired', '😩 Tired'),
    ]

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True)
    photo = models.ImageField(upload_to='habit_notes_photos/', blank=True, null=True)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'Note for {self.habit.name} on {self.date}'

