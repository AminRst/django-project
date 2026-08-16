from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTests(TestCase):
    def test_register_creates_user_with_hashed_password(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password': 'a-strong-test-password-123',
            'password2': 'a-strong-test-password-123',
            'email': 'newuser@example.com',
        })
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='newuser')
        # the raw password must never be stored as-is
        self.assertNotEqual(user.password, 'a-strong-test-password-123')
        self.assertTrue(user.check_password('a-strong-test-password-123'))

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'anotheruser',
            'password': 'password-one-123',
            'password2': 'password-two-456',
            'email': 'another@example.com',
        })
        self.assertContains(response, 'Passwords do not match')
        self.assertFalse(User.objects.filter(username='anotheruser').exists())


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='amin', password='correct-horse-battery')

    def test_login_with_correct_credentials_redirects_home(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'amin',
            'password': 'correct-horse-battery',
        })
        self.assertRedirects(response, reverse('accounts:home'))

    def test_login_with_wrong_password_shows_error(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'amin',
            'password': 'wrong-password',
        })
        self.assertContains(response, 'Invalid username or password')

    def test_inactive_user_cannot_log_in(self):
        # Note: Django's default ModelBackend already refuses to authenticate
        # inactive users (authenticate() returns None for them), so this hits
        # the same "Invalid username or password" branch as a wrong password
        # rather than the view's separate "account is not active" message.
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('accounts:login'), {
            'username': 'amin',
            'password': 'correct-horse-battery',
        })
        self.assertContains(response, 'Invalid username or password')
        self.assertFalse(response.wsgi_request.user.is_authenticated)
