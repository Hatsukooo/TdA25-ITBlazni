# api/serializer.py
from rest_framework import serializers
from .models import Game
from .constants import GAME_STATES, VALID_CHARACTERS, BOARD_SIZE

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['uuid', 'createdAt', 'updatedAt', 'name', 'difficulty', 'gameState', 'board']
        read_only_fields = ['uuid', 'createdAt', 'updatedAt']

    def validate_gameState(self, value):
        print(f"Validating gameState: {value}")  # Debug
        if value not in GAME_STATES.values():
            raise serializers.ValidationError("Invalid game state.")
        return value

    def validate_board(self, value):
        print(f"Validating board with {len(value)} rows.")  # Debug
        if len(value) != BOARD_SIZE:
            raise serializers.ValidationError(f"Board must have exactly {BOARD_SIZE} rows.")
        for row_index, row in enumerate(value):
            if len(row) != BOARD_SIZE:
                raise serializers.ValidationError(f"Row {row_index + 1} must have exactly {BOARD_SIZE} cells.")
            for col_index, cell in enumerate(row):
                if cell not in VALID_CHARACTERS:
                    raise serializers.ValidationError(f"Invalid cell value: '{cell}' at Row {row_index + 1}, Column {col_index + 1}. Allowed: {VALID_CHARACTERS}.")
        return value

    def validate(self, data):
        # Example: Additional validations can be placed here
        print(f"Validating entire game data: {data}")  # Debug
        return data