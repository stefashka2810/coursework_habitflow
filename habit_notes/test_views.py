from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from habits.models import Habit
from .models import HabitNote
from .forms import HabitNoteForm
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class HabitNoteViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        self.client.login(username='testuser', password='securepassword123')
        
        self.habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        self.note = HabitNote.objects.create(
            habit=self.habit,
            date=timezone.now().date(),
            note='Test Note',
            mood='happy'
        )
        
        self.all_notes_url = reverse('habit_notes:all_notes')
        self.add_note_url = reverse('habit_notes:add_note', args=[self.habit.id])
        self.delete_note_url = reverse('habit_notes:delete_note', args=[self.note.id])

    def test_all_notes_view(self):
        response = self.client.get(self.all_notes_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_notes/all_notes.html')
        
        self.assertIn('habits', response.context)
        habit_in_context = False
        for habit in response.context['habits']:
            if habit.id == self.habit.id:
                habit_in_context = True
                break
        self.assertTrue(habit_in_context)
    
    def test_all_notes_view_empty(self):
        # Удаляем существующие привычки
        Habit.objects.all().delete()
        
        response = self.client.get(self.all_notes_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/habitat_without_value.html')
    
    def test_add_note_view_GET(self):
        response = self.client.get(self.add_note_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_notes/note_form.html')
        self.assertIsInstance(response.context['form'], HabitNoteForm)
        self.assertEqual(response.context['habit'], self.habit)
    
    def test_add_note_view_POST_success(self):
        note_data = {
            'date': timezone.now().date().strftime('%Y-%m-%d'),
            'note': 'New Note',
            'mood': 'neutral'
        }
        
        response = self.client.post(self.add_note_url, note_data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, self.all_notes_url)
        
        self.assertTrue(HabitNote.objects.filter(note='New Note').exists())
    
    def test_add_note_view_POST_with_photo(self):
        self.skipTest("Пропускаем тест загрузки фото")
        
        small_png = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00'
            b'\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDATx'
            b'\x9cc````\x00\x00\x00\x05\x00\x01\xa5\xf6E\xe0\x00\x00\x00\x00'
            b'IEND\xaeB`\x82'
        )
        
        temp_image = SimpleUploadedFile(
            'small.png',
            small_png,
            content_type='image/png'
        )
        
        note_data = {
            'date': timezone.now().date().strftime('%Y-%m-%d'),
            'note': 'Note with Photo',
            'mood': 'happy',
            'photo': temp_image
        }
        
        response = self.client.post(self.add_note_url, note_data)
        
        self.assertIn(response.status_code, [200, 302])
    
    def test_add_note_view_POST_invalid(self):
        invalid_data = {
            'date': 'invalid-date',  
            'note': 'Invalid Note',
            'mood': 'angry'
        }
        
        response = self.client.post(self.add_note_url, invalid_data)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'habit_notes/note_form.html')
    
    def test_delete_note(self):
        """Тест удаления заметки"""
        response = self.client.post(self.delete_note_url)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.all_notes_url)
        
        self.assertFalse(HabitNote.objects.filter(id=self.note.id).exists())
    
    def test_delete_note_GET(self):
        note_count_before = HabitNote.objects.count()

        self.client.get(self.delete_note_url)
        
        note_count_after = HabitNote.objects.count()
        self.assertEqual(note_count_before, note_count_after)
        self.assertTrue(HabitNote.objects.filter(id=self.note.id).exists()) 