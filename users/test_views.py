from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from habits.models import Habit
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.registration_url = reverse('users:registration')
        self.profile_url = reverse('users:profile')
        self.logout_url = reverse('users:logout')
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        
        self.login_data = {
            'username': 'testuser',
            'password': 'securepassword123'
        }
        
        self.registration_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword456',
            'password2': 'securepassword456',
            'first_name': 'New',
            'last_name': 'User'
        }

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
    
    def test_login_view_POST_success(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('main:main_after_registration'))
    
    def test_login_view_POST_invalid(self):
        invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'users/registration.html')
    
    def test_registration_view_GET(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registr.html')
    
    def test_registration_view_POST_success(self):
        response = self.client.post(self.registration_url, self.registration_data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, self.login_url)
        
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_registration_view_POST_invalid(self):
        invalid_data = self.registration_data.copy()
        invalid_data['password2'] = 'differentpassword'
        
        response = self.client.post(self.registration_url, invalid_data)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'users/registr.html')
        
    def test_profile_view_authenticated(self):
        habit = Habit.objects.create(
            user=self.user,
            name='Test Habit',
            category='good',
            frequency='daily',
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        
        self.assertIn('habits', response.context)
        self.assertIn(habit, response.context['habits'])
    
    def test_logout_view(self):
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('main:index'))
        
        self.assertNotIn('_auth_user_id', self.client.session)
        
    
    def test_delete_account(self):
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.post(reverse('users:delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        
        self.assertFalse(User.objects.filter(username='testuser').exists()) 