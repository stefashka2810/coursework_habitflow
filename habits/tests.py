from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, date, timedelta
from .models import Habit, HabitCompletion

User = get_user_model()

class HabitModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.habit_data = {
            'user': self.user,
            'name': 'Test Habit',
            'description': 'This is a test habit',
            'category': 'good',
            'frequency': 'daily',
            'end_date': timezone.now().date() + timedelta(days=30),
        }
        
        self.habit = Habit.objects.create(**self.habit_data)

    def test_habit_creation(self):
        """Test that a habit can be created"""
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(self.habit.name, self.habit_data['name'])
        self.assertEqual(self.habit.description, self.habit_data['description'])
        self.assertEqual(self.habit.category, self.habit_data['category'])
        self.assertEqual(self.habit.frequency, self.habit_data['frequency'])
        self.assertEqual(self.habit.end_date, self.habit_data['end_date'])
        self.assertEqual(self.habit.user, self.user)
        self.assertIsNotNone(self.habit.created_at)
        self.assertIsNotNone(self.habit.updated_at)

    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f'Test Habit (good)'
        self.assertEqual(str(self.habit), expected_str)
        
    def test_habit_with_different_categories(self):
        """Test that habits can be created with different categories"""
        bad_habit = Habit.objects.create(
            user=self.user,
            name='Bad Habit',
            description='This is a bad habit',
            category='bad',
            frequency='weekly',
            end_date=timezone.now().date() + timedelta(days=60),
        )
        
        self.assertEqual(bad_habit.category, 'bad')
        self.assertEqual(str(bad_habit), 'Bad Habit (bad)')
        
    def test_habit_with_different_frequencies(self):
        """Test that habits can be created with different frequencies"""
        frequencies = ['daily', 'weekly', 'biweekly', 'monthly', 'semiannual', 'yearly']
        
        for freq in frequencies:
            habit = Habit.objects.create(
                user=self.user,
                name=f'{freq.capitalize()} Habit',
                category='good',
                frequency=freq,
                end_date=timezone.now().date() + timedelta(days=90),
            )
            
            self.assertEqual(habit.frequency, freq)


class HabitCompletionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30),
        )
        
        self.today = timezone.now().date()
        self.completion = HabitCompletion.objects.create(
            habit=self.habit,
            date=self.today,
            completed=True
        )

    def test_completion_creation(self):
        """Test that a habit completion can be created"""
        self.assertEqual(HabitCompletion.objects.count(), 1)
        self.assertEqual(self.completion.habit, self.habit)
        self.assertEqual(self.completion.date, self.today)
        self.assertTrue(self.completion.completed)

    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f'Habit: Test Habit | {self.today} | Completed: True'
        self.assertEqual(str(self.completion), expected_str)
    
    def test_unique_together_constraint(self):
        """Test that a habit can't have multiple completions for the same date"""
        with self.assertRaises(Exception):
            HabitCompletion.objects.create(
                habit=self.habit,
                date=self.today,
                completed=False
            )
    
    def test_update_completion_status(self):
        """Test that a habit completion status can be updated"""
        self.completion.completed = False
        self.completion.save()
        
        updated_completion = HabitCompletion.objects.get(habit=self.habit, date=self.today)
        self.assertFalse(updated_completion.completed)
