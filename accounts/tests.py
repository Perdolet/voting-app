from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthSystemTest(APITestCase):

    def setUp(self) -> None:
        self.created_user = User.objects.create_user(
            username='test_user',
            password='123456qwerty',
            email='test_email@test.com'
        )
        self.created_user_token = str(
            Token.objects.create(user=self.created_user)
        )

    def test_registration_success(self):
        url = '/auth/register/'
        data = {
            'username': 'test_user2',
            'password': '123456qwerty123',
            'password2': '123456qwerty123',
            'email': 'test_email2@test.com',
            'first_name': 'test',
            'last_name': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_fail(self):
        url = '/auth/register/'
        data = {
            'username': 'test_user',
            'password': '123456',
            'password2': '123456',
            'email': 'test_email@test.com',
            'first_name': 'test',
            'last_name': 'test'
        }
        response = self.client.post(url, data, format='json')
        username_error = response.data.get('username')[0]
        password_errors = response.data.get('password')
        email_error = response.data.get('email')[0]
        self.assertEqual(username_error, 'This field must be unique.')
        self.assertEqual(
            password_errors[0],
            'This password is too short. It must contain at least 8 characters.'
        )
        self.assertEqual(
            password_errors[1],
            'This password is too common.'
        )
        self.assertEqual(
            password_errors[2],
            'This password is entirely numeric.'
        )
        self.assertEqual(email_error, 'This field must be unique.')

    def test_user_login_success(self):
        url = '/auth/login/'
        data = {
            'username': 'test_user',
            'password': '123456qwerty'
        }
        response = self.client.post(url, data, format='json')
        self.assertTrue(response.data.get('token'))

    def test_user_logout(self):
        url = '/auth/logout/'
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.created_user_token}'
        )
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
