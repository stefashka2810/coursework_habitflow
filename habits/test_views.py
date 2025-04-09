from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Habit, HabitCompletion
from .forms import HabitForm
from django.utils import timezone
from datetime import timedelta, date
import json

User = get_user_model()

class HabitViewsTests(TestCase):
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
            description='Test Description',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        self.create_habit_url = reverse('habits:create_habit')
        self.habit_list_url = reverse('habits:habit_list')
        self.habit_tracker_url = reverse('habits:habit_tracker', args=[self.habit.id])
        self.toggle_completion_url = reverse('habits:toggle_completion', args=[self.habit.id])
        self.delete_habit_url = reverse('habits:delete_habit', args=[self.habit.id])

    def test_create_habit_view_GET(self):
        response = self.client.get(self.create_habit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/add_habitat.html')
        self.assertIsInstance(response.context['form'], HabitForm)
    
    def test_create_habit_view_POST_success(self):
        habit_data = {
            'name': 'New Habit',
            'description': 'New Description',
            'category': 'bad',
            'frequency': 'weekly',
            'end_date': (timezone.now().date() + timedelta(days=60)).strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.create_habit_url, habit_data)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.habit_list_url)
        
        self.assertTrue(Habit.objects.filter(name='New Habit').exists())
    
    def test_create_habit_view_POST_invalid(self):
        invalid_data = {
            'name': '',  
            'category': 'good',
            'frequency': 'daily',
            'end_date': (timezone.now().date() + timedelta(days=30)).strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.create_habit_url, invalid_data)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'habits/add_habitat.html')
        
    def test_habit_list_view(self):
        response = self.client.get(self.habit_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/list_habitats.html')
        
        self.assertIn('habits', response.context)
        self.assertIn(self.habit, response.context['habits'])
        
    def test_habit_list_view_empty(self):
        Habit.objects.all().delete()
        
        response = self.client.get(self.habit_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/habitat_without_value.html')
    
    def test_habit_tracker_view(self):
        response = self.client.get(self.habit_tracker_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/habit_tracker.html')
        
        self.assertIn('habit', response.context)
        self.assertIn('dates_list', response.context)
        self.assertIn('completed_dates', response.context)
        self.assertEqual(response.context['habit'], self.habit)
    
    def test_toggle_completion(self):
        today = timezone.now().date()
        data = {
            'date': today.strftime('%Y-%m-%d'),
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
        
        completion = HabitCompletion.objects.get(habit=self.habit, date=today)
        self.assertTrue(completion.completed)
        
        data['completed'] = False
        response = self.client.post(
            self.toggle_completion_url,
            json.dumps(data),
            content_type='application/json'
        )
        
        completion.refresh_from_db()
        self.assertFalse(completion.completed)
    
    def test_delete_habit(self):
        response = self.client.post(self.delete_habit_url)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.habit_list_url)
        
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())
    
    def test_delete_habit_GET(self):
        response = self.client.get(self.delete_habit_url)
        self.assertEqual(response.status_code, 400)
        
        self.assertTrue(Habit.objects.filter(id=self.habit.id).exists()) 