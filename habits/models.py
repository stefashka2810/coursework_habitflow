from django.db import models
from django.conf import settings

class Habit(models.Model):
    GOOD_OR_BAD_CHOICES = (
        ('good', 'Good'),
        ('bad', 'Bad'),
    )

    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Every 2 Weeks'),
        ('monthly', 'Monthly'),
        ('semiannual', 'Every 6 Months'),
        ('yearly', 'Yearly'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits'
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=4, choices=GOOD_OR_BAD_CHOICES)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name} ({self.category})'
