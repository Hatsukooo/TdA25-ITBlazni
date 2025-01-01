from rest_framework import serializers
from .models import Game
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['uuid', 'name', 'difficulty', 'board', 'gameState', 'created_at', 'updated_at']

    def validate_board(self, value):
        if len(value) != 15 or any(len(row) != 15 for row in value):
            raise serializers.ValidationError("Board must be a 15x15 grid.")
        return value

