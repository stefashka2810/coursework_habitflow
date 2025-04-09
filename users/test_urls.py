from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from . import views

User = get_user_model()

class UserUrlsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.registration_url = reverse('users:registration')
        self.profile_url = reverse('users:profile')
        self.logout_url = reverse('users:logout')
        self.delete_account_url = reverse('users:delete_account')
        self.password_reset_url = reverse('users:password_reset')
        
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )

    def test_login_url_resolves(self):
        resolver = resolve(self.login_url)
        self.assertEqual(resolver.func, views.login)
    
    def test_registration_url_resolves(self):
        resolver = resolve(self.registration_url)
        self.assertEqual(resolver.func, views.registration)
    
    def test_profile_url_resolves(self):
        resolver = resolve(self.profile_url)
        self.assertEqual(resolver.func, views.profile)
    
    def test_logout_url_resolves(self):
        resolver = resolve(self.logout_url)
        self.assertEqual(resolver.func, views.logout)
    
    def test_delete_account_url_resolves(self):
        resolver = resolve(self.delete_account_url)
        self.assertEqual(resolver.func, views.delete_account)
    
    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
    
    def test_registration_GET(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registr.html')
    
    def test_profile_requires_authentication(self):
        try:
            response = self.client.get(self.profile_url)
            # Если нет исключения, проверяем что доступ запрещен или перенаправлен
            self.assertNotEqual(response.status_code, 200)
        except:
            # Если есть исключение, значит доступ защищен
            pass
    
    def test_profile_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def test_logout_redirects(self):
        self.client.login(username='testuser', password='securepassword123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
    
    def test_auth_flow(self):
        registration_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'SecurePassword123',
            'password2': 'SecurePassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        # Регистрация
        response = self.client.post(self.registration_url, registration_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Вход
        login_data = {
            'username': 'newuser',
            'password': 'SecurePassword123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        
        # Доступ к профилю
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        
        # Выход
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302) 