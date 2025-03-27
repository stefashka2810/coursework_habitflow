# from django.db import models
# from django.contrib.auth import get_user_model
# from django.core.validators import MinLengthValidator
# from django.utils import timezone
# from django.core.exceptions import ValidationError

# User = get_user_model()

# class Habit(models.Model):
#     class Category(models.TextChoices):
#         GOOD = 'Good', 'Good'
#         BAD = 'Bad', 'Bad'
    
#     class Frequency(models.TextChoices):
#         DAILY = 'Daily', 'Daily'
#         WEEKLY = 'Weekly', 'Weekly'
#         TWO_WEEKS = 'Every 2 Weeks', 'Every 2 Weeks'
#         MONTHLY = 'Monthly', 'Monthly'
#         SIX_MONTHS = 'Every 6 Months', 'Every 6 Months'
#         YEARLY = 'Yearly', 'Yearly'
    
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='habits'
#     )
    
#     title = models.CharField(
#         max_length=100,
#         validators=[MinLengthValidator(3)],
#         help_text="Name of your habit"
#     )
    
#     category = models.CharField(
#         max_length=20,
#         choices=Category.choices,
#         default=Category.GOOD
#     )
    
#     description = models.TextField(
#         blank=True,
#         null=True,
#         help_text="Optional description"
#     )
    
#     frequency = models.CharField(
#         max_length=20,
#         choices=Frequency.choices,
#         default=Frequency.DAILY
#     )
    
#     end_date = models.DateField(
#         help_text="When should this habit end?"
#     )
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = 'Habit'
#         verbose_name_plural = 'Habits'
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'title'],
#                 name='unique_user_habit'
#             )
#         ]

#     def __str__(self):
#         return f"{self.title} ({self.get_category_display()})"

#     def clean(self):
#         super().clean()
        
#         # Validate end date
#         if self.end_date < timezone.now().date():
#             raise ValidationError({'end_date': 'End date cannot be in the past'})

#     def save(self, *args, **kwargs):
#         """Auto-update is_active status on save"""
#         self.is_active = self.end_date >= timezone.now().date()
#         super().save(*args, **kwargs)

#     def get_frequency_days(self):
#         """Convert frequency to days for reminder calculations"""
#         frequency_map = {
#             self.Frequency.DAILY: 1,
#             self.Frequency.WEEKLY: 7,
#             self.Frequency.TWO_WEEKS: 14,
#             self.Frequency.MONTHLY: 30,
#             self.Frequency.SIX_MONTHS: 180,
#             self.Frequency.YEARLY: 365
#         }
#         return frequency_map.get(self.frequency, 1)