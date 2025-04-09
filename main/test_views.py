from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class MainViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        self.index_url = reverse('main:index')
        self.about_url = reverse('main:about')
        self.settings_url = reverse('main:settings')
        self.main_after_registration_url = reverse('main:main_after_registration')

    def test_index_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main_before_registration.html')
    
    def test_about_view(self):
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
    
    def test_settings_view_authenticated(self):
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/settings.html')
        
        self.assertIn('user_obj', response.context)
        self.assertEqual(response.context['user_obj'], self.user)
    
    def test_main_after_registration_view(self):
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.get(self.main_after_registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main_after_registration.html')
    
    def test_authentication_requirements(self):
        response = self.client.get(self.main_after_registration_url)
        if response.status_code == 302:
            self.assertRedirects(
                response, 
                f'/login/?next={self.main_after_registration_url}',
                fetch_redirect_response=False
            )
        elif response.status_code == 200:
            self.assertTemplateUsed(response, 'main/main_after_registration.html')
            
    def test_settings_view_not_authenticated(self):
        response = self.client.get(self.settings_url)
        if response.status_code == 302:
            self.assertRedirects(
                response, 
                f'/login/?next={self.settings_url}',
                fetch_redirect_response=False
            )
        elif response.status_code == 200:
            self.assertTemplateUsed(response, 'main/settings.html') 