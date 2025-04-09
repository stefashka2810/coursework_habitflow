from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_email_unique(self):
        duplicate_user_data = self.user_data.copy()
        duplicate_user_data['username'] = 'anotheruser'
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)

    def test_get_display_name(self):
        self.assertEqual(self.user.get_display_name(), 'Test User')
        
        user_no_name = User.objects.create_user(
            username='noname',
            email='noname@example.com',
            password='password123'
        )
        self.assertEqual(user_no_name.get_display_name(), 'noname')

    def test_str_method(self):
        expected_str = f'Test User (test@example.com)'
        self.assertEqual(str(self.user), expected_str)
