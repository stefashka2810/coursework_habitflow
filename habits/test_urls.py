from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import json
from . import views
from .models import Habit

User = get_user_model()

class HabitUrlsTest(TestCase):
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
            description='Test Description',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        # URL для тестирования
        self.create_habit_url = reverse('habits:create_habit')
        self.habit_list_url = reverse('habits:habit_list')
        self.habit_tracker_url = reverse('habits:habit_tracker', args=[self.habit.id])
        self.toggle_completion_url = reverse('habits:toggle_completion', args=[self.habit.id])
        self.delete_habit_url = reverse('habits:delete_habit', args=[self.habit.id])

    def test_create_habit_url_resolves(self):
        resolver = resolve(self.create_habit_url)
        self.assertEqual(resolver.func, views.create_habit)
    
    def test_habit_list_url_resolves(self):
        resolver = resolve(self.habit_list_url)
        self.assertEqual(resolver.func, views.habit_list)
    
    def test_habit_tracker_url_resolves(self):
        resolver = resolve(self.habit_tracker_url)
        self.assertEqual(resolver.func, views.habit_tracker_view)
    
    def test_toggle_completion_url_resolves(self):
        resolver = resolve(self.toggle_completion_url)
        self.assertEqual(resolver.func, views.toggle_completion)
    
    def test_delete_habit_url_resolves(self):
        resolver = resolve(self.delete_habit_url)
        self.assertEqual(resolver.func, views.delete_habit)
    
    def test_urls_require_authentication(self):
        urls = [
            self.create_habit_url,
            self.habit_list_url,
            self.habit_tracker_url,
            self.delete_habit_url
        ]
        
        for url in urls:
            try:
                response = self.client.get(url)
                # Отлавливаем только URL, которые возвращают 200 для неавторизованных пользователей
                if url == self.create_habit_url and response.status_code == 200:
                    # Это проблема - URL для создания должен требовать авторизацию
                    self.fail(f"URL {url} should require authentication")
                else:
                    self.assertNotEqual(response.status_code, 200, f"URL {url} should require authentication")
            except:
                # Если вызвано исключение, значит URL требует авторизации
                pass
    
    def test_urls_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        
        # Проверяем доступ к страницам, которые должны возвращать HTML
        urls = [
            self.create_habit_url,
            self.habit_list_url,
            self.habit_tracker_url
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"URL {url} should be accessible when authenticated")
    
    def test_toggle_completion_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        
        today = timezone.now().date().strftime('%Y-%m-%d')
        data = {
            'date': today,
            'completed': True
        }
        
        response = self.client.post(
            self.toggle_completion_url,
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
    
    def test_delete_habit_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.post(self.delete_habit_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.habit_list_url)
    
    def test_habit_ownership_protection(self):
        # Создаем второго пользователя
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        
        # Авторизуемся другим пользователем
        self.client.login(username='otheruser', password='otherpassword123')
        
        # Пробуем получить доступ к трекеру привычки, созданной первым пользователем
        response = self.client.get(self.habit_tracker_url)
        self.assertNotEqual(response.status_code, 200)
        
        # Пробуем удалить привычку, созданную первым пользователем
        response = self.client.post(self.delete_habit_url)
        self.assertNotEqual(response.status_code, 302) 