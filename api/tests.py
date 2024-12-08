from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class GameAPITest(APITestCase):
    def test_create_game(self):
        url = '/api/v1/games/'
        data = {
            "name": "Moje první hra",
            "difficulty": "hard",
            "board": [[""] * 15] * 15  # 15x15 prázdná deska
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Moje první hra')
        self.assertEqual(response.data['difficulty'], 'hard')
        self.assertTrue('board' in response.data)
