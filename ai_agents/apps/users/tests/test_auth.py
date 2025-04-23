from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('users_api:auth_register')
        self.login_url = reverse('users_api:auth_login')
        self.user_detail_url = reverse('users_api:user_detail')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }

    def test_user_registration(self):
        """Ensure we can register a new user."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'test@example.com')

    def test_user_login(self):
        """Ensure registered user can log in and get tokens."""
        # First, register the user
        self.client.post(self.register_url, self.user_data, format='json')

        login_data = {'email': self.user_data['email'], 'password': self.user_data['password']}
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_user_details_authenticated(self):
        """Ensure authenticated user can access their details."""
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {'email': self.user_data['email'], 'password': self.user_data['password']}
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']

        # Authenticate the request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.user_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_get_user_details_unauthenticated(self):
        """Ensure unauthenticated user cannot access user details."""
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)