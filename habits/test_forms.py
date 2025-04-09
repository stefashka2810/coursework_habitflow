from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .forms import HabitForm
from .models import Habit
from django.contrib.auth import get_user_model

User = get_user_model()

class HabitFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        self.valid_data = {
            'name': 'Test Habit',
            'description': 'Test Habit Description',
            'category': 'good',
            'frequency': 'daily',
            'end_date': (timezone.now().date() + timedelta(days=30)).strftime('%Y-%m-%d')
        }

    def test_form_valid_data(self):
        form = HabitForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
    def test_blank_data(self):
        form = HabitForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)  
        
    def test_invalid_category(self):
        data = self.valid_data.copy()
        data['category'] = 'invalid'
        form = HabitForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        
    def test_invalid_frequency(self):
        data = self.valid_data.copy()
        data['frequency'] = 'invalid'
        form = HabitForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('frequency', form.errors)
        
    def test_past_end_date(self):
        data = self.valid_data.copy()
        data['end_date'] = (timezone.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
        form = HabitForm(data=data)
       
    def test_save_form(self):
        form = HabitForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        habit = form.save(commit=False)
        habit.user = self.user
        habit.save()
        
        self.assertEqual(habit.name, 'Test Habit')
        self.assertEqual(habit.description, 'Test Habit Description')
        self.assertEqual(habit.category, 'good')
        self.assertEqual(habit.frequency, 'daily')
        self.assertEqual(habit.user, self.user)
        
    def test_required_fields(self):
        required_fields = ['name', 'category', 'frequency', 'end_date']
        
        for field in required_fields:
            with self.subTest(field=field):
                data = self.valid_data.copy()
                data[field] = ''
                form = HabitForm(data=data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors) 