from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from habits.models import Habit
from .models import HabitNote
from .forms import HabitNoteForm
from django import forms

User = get_user_model()

class HabitNoteFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        self.valid_data = {
            'date': timezone.now().date().strftime('%Y-%m-%d'),
            'note': 'Test Note Content',
            'mood': 'happy'
        }
        
        self.small_png = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00'
            b'\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDATx'
            b'\x9cc````\x00\x00\x00\x05\x00\x01\xa5\xf6E\xe0\x00\x00\x00\x00'
            b'IEND\xaeB`\x82'
        )

    def test_form_valid_data(self):
        form = HabitNoteForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
    def test_blank_data(self):
        form = HabitNoteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        
    def test_invalid_date_format(self):
        data = self.valid_data.copy()
        data['date'] = 'invalid-date'
        form = HabitNoteForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        
    def test_invalid_mood(self):
        data = self.valid_data.copy()
        data['mood'] = 'invalid-mood'
        form = HabitNoteForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('mood', form.errors)
        
    def test_save_form(self):
        form = HabitNoteForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        note = form.save(commit=False)
        note.habit = self.habit
        note.save()
        
        self.assertEqual(note.note, 'Test Note Content')
        self.assertEqual(note.mood, 'happy')
        self.assertEqual(note.habit, self.habit)
        
    def test_date_required(self):
        data = self.valid_data.copy()
        data.pop('date')
        form = HabitNoteForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        
    def test_form_widgets(self):
        form = HabitNoteForm()
        self.assertIsInstance(form.fields['date'].widget, forms.DateInput)
        self.assertEqual(form.fields['note'].widget.attrs.get('rows'), 4) 