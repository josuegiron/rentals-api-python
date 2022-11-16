from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, Token

import json


class RegisterUser(APITestCase):
    def test_register_user(self):
        url = '/api/users/'
        data = {'email': 'enriquedescamps@gmail.com', 'first_name': 'Enrique', 'last_name': 'Descamps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_user(self):
        url = '/api/users/'
        data = {'email': 'enriquedescamps@gmail.com', 'first_name': 'Enrique', 'last_name': 'Descamps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/users/'
        data = {'email': 'enriquedescamps@gmail.com', 'first_name': 'Enrique', 'last_name': 'Descamps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUser(APITestCase):
    def test_generate_token(self):
        url = '/api/users/'
        data = {'email': 'enriquedescamps@gmail.com', 'first_name': 'Enrique', 'last_name': 'Descamps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/users/tokens/'
        data = {'email': 'enriquedescamps@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = '/api/users/'
        data = {'email': 'enriquedescamps@gmail.com', 'first_name': 'Enrique', 'last_name': 'Descamps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/users/tokens/'
        data = {'email': 'enriquedescamps@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        token = Token.objects.get(user__email='enriquedescamps@gmail.com')

        url = '/api/users/login/'
        data = {'email': 'enriquedescamps@gmail.com', 'token': str(token.token)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


class CreateSearch(APITestCase):
    def test_search(self):
        url = '/api/users/'
        data = {'email': 'enriquedescamps@gmail.com', 'first_name': 'Enrique', 'last_name': 'Descamps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email='enriquedescamps@gmail.com')

        filters = {'type__name__in':['House', 'Apartment'], 'area__ameninties__name__in':['Television', 'Washer']}
        url = '/api/users/search/'
        data = {'user': user.id, 'filters':json.dumps(filters)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
