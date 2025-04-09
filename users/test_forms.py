from django.test import TestCase
from .forms import UserRegisterForm, UserLoginForm, ForgotPasswordForm
from .models import User

class UserRegisterFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='password123'
        )

    def test_form_valid_data(self):
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
    def test_blank_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6) 
        
    def test_passwords_not_matching(self):
        data = self.valid_data.copy()
        data['password2'] = 'differentpassword123'
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
    def test_username_already_exists(self):
        data = self.valid_data.copy()
        data['username'] = 'existinguser'
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    def test_email_already_exists(self):
        data = self.valid_data.copy()
        data['email'] = 'existing@example.com'
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    def test_save_form(self):
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('securepassword123'))

class UserLoginFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        self.valid_data = {
            'username': 'testuser',
            'password': 'securepassword123'
        }

    def test_form_valid_data(self):
        form = UserLoginForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
    def test_blank_data(self):
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  

class ForgotPasswordFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'new_password': 'newsecurepassword123'
        }

    def test_form_valid_data(self):
        form = ForgotPasswordForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
    def test_blank_data(self):
        form = ForgotPasswordForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2) 
        
    def test_password_too_short(self):
        data = self.valid_data.copy()
        data['new_password'] = 'short'
        form = ForgotPasswordForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password', form.errors) 