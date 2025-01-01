# api/tests.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Game

class GameAPITests(TestCase):
    def setUp(self):
        """Setup the test environment by creating a sample game."""
        self.client = APIClient()
        self.game_data = {
            'name': 'Tic-Tac-Toe',
            'difficulty': 'easy',
            'board': [[None]*15 for _ in range(15)],  # Updated to 15x15 empty board
        }
        self.game = Game.objects.create(**self.game_data)

    def test_create_game(self):
        """Test the creation of a new game through the API."""
        response = self.client.post('/api/v1/games/', self.game_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  # Debug information
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 2)

    def test_get_game_list(self):
        """Test retrieving the list of games through the API."""
        response = self.client.get('/api/v1/games/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure there is at least one game

    def test_get_game_detail(self):
        """Test retrieving a single game through the API."""
        response = self.client.get(f'/api/v1/games/{self.game.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.game.name)

    def test_update_game(self):
        """Test updating an existing game through the API."""
        updated_data = {
            'name': 'Updated Tic-Tac-Toe',
            'difficulty': 'medium',
            'board': [[None]*15 for _ in range(15)],  # Updated to 15x15 empty board
        }
        response = self.client.put(f'/api/v1/games/{self.game.id}/', updated_data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(response.data)  # Debug information
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game.refresh_from_db()
        self.assertEqual(self.game.name, 'Updated Tic-Tac-Toe')

    def test_delete_game(self):
        """Test deleting an existing game through the API."""
        response = self.client.delete(f'/api/v1/games/{self.game.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Game.objects.count(), 0)  # After deletion, count should be 0

