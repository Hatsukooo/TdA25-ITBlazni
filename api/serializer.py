from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['uuid', 'name', 'difficulty', 'board', 'game_state', 'created_at', 'updated_at']