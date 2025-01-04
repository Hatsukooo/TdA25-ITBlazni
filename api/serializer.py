# api/serializers.py
from rest_framework import serializers
from .models import Game
from .constants import GAME_STATES, VALID_CHARACTERS, BOARD_SIZE

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['uuid', 'createdAt', 'updatedAt', 'name', 'difficulty', 'gameState', 'board']
        read_only_fields = ['uuid', 'createdAt', 'updatedAt']

    def validate_gameState(self, value):
        if value not in GAME_STATES.values():
            raise serializers.ValidationError("Invalid game state.")
        return value

    def validate_board(self, value):
        if len(value) != BOARD_SIZE:
            raise serializers.ValidationError(f"Board must have exactly {BOARD_SIZE} rows.")
        for row in value:
            if len(row) != BOARD_SIZE:
                raise serializers.ValidationError(f"Each row must have exactly {BOARD_SIZE} cells.")
            for cell in row:
                if cell not in VALID_CHARACTERS:
                    raise serializers.ValidationError(f"Invalid cell value: '{cell}'. Allowed: {VALID_CHARACTERS}.")
        return value

    def validate(self, data):
        # Example: Validate starting player if applicable
        # starting_player = data.get('startingPlayer', None)
        # if starting_player not in ['X', 'O']:
        #     raise serializers.ValidationError({"startingPlayer": "Starting player must be 'X' or 'O'."})
        return data