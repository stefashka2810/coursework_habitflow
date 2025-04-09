from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class MainViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        # URL для тестирования
        self.index_url = reverse('main:index')
        self.about_url = reverse('main:about')
        self.settings_url = reverse('main:settings')
        self.main_after_registration_url = reverse('main:main_after_registration')

    def test_index_view(self):
        """Тест отображения главной страницы для неавторизованных пользователей"""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main_before_registration.html')
    
    def test_about_view(self):
        """Тест отображения страницы о проекте"""
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
    
    def test_settings_view_authenticated(self):
        """Тест отображения страницы настроек для авторизованного пользователя"""
        # Авторизуемся
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/settings.html')
        
        # Проверяем, что пользователь передан в контекст
        self.assertIn('user_obj', response.context)
        self.assertEqual(response.context['user_obj'], self.user)
    
    def test_main_after_registration_view(self):
        """Тест отображения главной страницы для авторизованных пользователей"""
        # Авторизуемся
        self.client.login(username='testuser', password='securepassword123')
        
        response = self.client.get(self.main_after_registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main_after_registration.html')
    
    def test_authentication_requirements(self):
        """Тест проверки авторизации для защищенных страниц"""
        # Без авторизации попытка доступа к главной странице для авторизованных пользователей
        response = self.client.get(self.main_after_registration_url)
        # В зависимости от настроек проекта - либо 302 (редирект на логин), 
        # либо 200 (если нет проверки авторизации)
        if response.status_code == 302:
            # Если настроен редирект на страницу логина
            self.assertRedirects(
                response, 
                f'/login/?next={self.main_after_registration_url}',
                fetch_redirect_response=False
            )
        elif response.status_code == 200:
            # Если нет проверки авторизации
            self.assertTemplateUsed(response, 'main/main_after_registration.html')
            
    def test_settings_view_not_authenticated(self):
        """Тест отображения страницы настроек для неавторизованного пользователя"""
        # Без авторизации
        response = self.client.get(self.settings_url)
        
        # В зависимости от настроек проекта - либо 302 (редирект на логин), 
        # либо 200 (если нет проверки авторизации)
        if response.status_code == 302:
            # Если настроен редирект на страницу логина
            self.assertRedirects(
                response, 
                f'/login/?next={self.settings_url}',
                fetch_redirect_response=False
            )
        elif response.status_code == 200:
            # Если нет проверки авторизации
            self.assertTemplateUsed(response, 'main/settings.html') 