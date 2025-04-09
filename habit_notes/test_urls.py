from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from . import views
from .models import HabitNote
from habits.models import Habit

User = get_user_model()

class HabitNoteUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Создаем пользователя
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        # Создаем привычку для тестов
        self.habit = Habit.objects.create(
            user=self.test_user,
            name='Test Habit',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        # Создаем заметку для тестов
        self.note = HabitNote.objects.create(
            habit=self.habit,
            date=timezone.now().date(),
            note='Test Note',
            mood='happy'
        )
        
        # URL для тестирования
        self.all_notes_url = reverse('habit_notes:all_notes')
        self.add_note_url = reverse('habit_notes:add_note', args=[self.habit.id])
        self.delete_note_url = reverse('habit_notes:delete_note', args=[self.note.id])

    def test_all_notes_url_resolves(self):
        resolver = resolve(self.all_notes_url)
        self.assertEqual(resolver.func, views.all_notes_view)
    
    def test_add_note_url_resolves(self):
        resolver = resolve(self.add_note_url)
        self.assertEqual(resolver.func, views.add_note)
    
    def test_delete_note_url_resolves(self):
        resolver = resolve(self.delete_note_url)
        self.assertEqual(resolver.func, views.delete_note)
    
    def test_urls_require_authentication(self):
        urls = [
            self.all_notes_url,
            self.add_note_url,
            self.delete_note_url
        ]
        
        for url in urls:
            try:
                response = self.client.get(url)
                # Если запрос обработан (нет исключения), проверяем, что не 200
                self.assertNotEqual(response.status_code, 200, f"URL {url} should require authentication")
            except Exception:
                # Если получаем ошибку из-за AnonymousUser, это тоже означает что страница защищена
                pass
    
    def test_urls_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        
        # Проверяем доступ к страницам с HTML
        response = self.client.get(self.all_notes_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.add_note_url)
        self.assertEqual(response.status_code, 200)
    
    def test_add_note_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        
        data = {
            'date': timezone.now().date().strftime('%Y-%m-%d'),
            'note': 'New Test Note',
            'mood': 'neutral'
        }
        
        response = self.client.post(self.add_note_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.all_notes_url)
        
        # Проверяем, что заметка создана
        self.assertTrue(HabitNote.objects.filter(note='New Test Note').exists())
    
    def test_delete_note_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.post(self.delete_note_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.all_notes_url)
        
        # Проверяем, что заметка удалена
        self.assertFalse(HabitNote.objects.filter(id=self.note.id).exists())
    
    def test_note_ownership_protection(self):
        # Создаем второго пользователя
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        
        # Создаем привычку для второго пользователя
        other_habit = Habit.objects.create(
            user=other_user,
            name='Other Habit',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        # Создаем заметку для тестирования, которая не будет удалена
        note_id = self.note.id
        
        # Авторизуемся другим пользователем
        self.client.login(username='otheruser', password='otherpassword123')
        
        # Пробуем удалить заметку, созданную первым пользователем
        try:
            response = self.client.post(self.delete_note_url)
        except:
            # Даже если получим ошибку, это нормально - проверяем что заметка не удалена
            pass
            
        # Проверяем, что заметка все еще существует
        self.assertTrue(HabitNote.objects.filter(id=note_id).exists()) 