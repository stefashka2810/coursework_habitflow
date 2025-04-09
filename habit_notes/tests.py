from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta
import tempfile
import os
from habits.models import Habit
from .models import HabitNote

User = get_user_model()

class HabitNoteModelTests(TestCase):
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
        
        self.note_data = {
            'habit': self.habit,
            'date': self.today,
            'note': 'This is a test note',
            'mood': 'happy'
        }
        
        self.note = HabitNote.objects.create(**self.note_data)

    def test_habit_note_creation(self):
        """Test that a habit note can be created"""
        self.assertEqual(HabitNote.objects.count(), 1)
        self.assertEqual(self.note.habit, self.habit)
        self.assertEqual(self.note.date, self.today)
        self.assertEqual(self.note.note, self.note_data['note'])
        self.assertEqual(self.note.mood, self.note_data['mood'])
        self.assertFalse(bool(self.note.photo))
        self.assertIsNotNone(self.note.created_at)

    def test_str_method(self):
        """Test the __str__ method"""
        expected_str = f'Note for Test Habit on {self.today}'
        self.assertEqual(str(self.note), expected_str)
    
    def test_habit_note_with_different_moods(self):
        """Test that notes can be created with different moods"""
        moods = ['happy', 'neutral', 'sad', 'angry', 'tired']
        
        for idx, mood in enumerate(moods):
            note = HabitNote.objects.create(
                habit=self.habit,
                date=self.today - timedelta(days=idx+1),
                note=f'This is a {mood} note',
                mood=mood
            )
            
            self.assertEqual(note.mood, mood)
    
    def test_note_without_mood(self):
        """Test that notes can be created without mood"""
        note = HabitNote.objects.create(
            habit=self.habit,
            date=self.today - timedelta(days=7),
            note='This is a note without mood'
        )
        
        self.assertEqual(note.mood, '')
    
    def test_habit_note_ordering(self):
        """Test that habit notes are ordered by date in descending order"""
        # Create two more notes with different dates
        yesterday = self.today - timedelta(days=1)
        tomorrow = self.today + timedelta(days=1)
        
        HabitNote.objects.create(
            habit=self.habit,
            date=yesterday,
            note='Yesterday note'
        )
        
        HabitNote.objects.create(
            habit=self.habit,
            date=tomorrow,
            note='Tomorrow note'
        )
        
        notes = HabitNote.objects.all()
        self.assertEqual(notes[0].date, tomorrow)
        self.assertEqual(notes[1].date, self.today)
        self.assertEqual(notes[2].date, yesterday)
    
    def test_habit_note_with_photo(self):
        """Test that notes can include a photo"""
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_img:
            temp_img.write(b'dummy image content')
            temp_img.seek(0)
            
            # Create a note with a photo
            photo_note = HabitNote.objects.create(
                habit=self.habit,
                date=self.today - timedelta(days=10),
                note='Note with photo',
                photo=SimpleUploadedFile(
                    name='test_image.jpg',
                    content=temp_img.read(),
                    content_type='image/jpeg'
                )
            )
            
            self.assertIsNotNone(photo_note.photo)
            
            # Clean up the uploaded file
            if photo_note.photo and os.path.isfile(photo_note.photo.path):
                os.remove(photo_note.photo.path)
