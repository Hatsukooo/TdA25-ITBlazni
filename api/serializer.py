from rest_framework import serializers
from .models import Game
from django.utils import timezone
import uuid
import re

class GameSerializer(serializers.ModelSerializer):
    # Constants
    DIFFICULTY_CHOICES = ['easy', 'medium', 'hard']
    GAME_STATE_CHOICES = ['opening', 'midgame', 'endgame']
    BOARD_SIZE = 15
    VALID_MOVES = ['X', 'O', '']

    # Field definitions with custom error messages
    uuid = serializers.UUIDField(
        required=False,
        error_messages={
            'invalid': 'Invalid UUID format.',
            'unique': 'Game with this UUID already exists.'
        }
    )
    createdAt = serializers.DateTimeField(read_only=True)
    updatedAt = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(
        max_length=100,
        error_messages={
            'required': 'Game name is required.',
            'blank': 'Game name cannot be blank.',
            'max_length': 'Game name cannot exceed 100 characters.',
            'invalid': 'Game name contains invalid characters.'
        }
    )
    difficulty = serializers.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        error_messages={
            'required': 'Difficulty level is required.',
            'invalid_choice': 'Difficulty must be one of: easy, medium, hard.'
        }
    )
    gameState = serializers.ChoiceField(
        choices=GAME_STATE_CHOICES,
        error_messages={
            'required': 'Game state is required.',
            'invalid_choice': 'Game state must be one of: opening, midgame, endgame.'
        }
    )
    board = serializers.ListField(
        child=serializers.ListField(
            child=serializers.ChoiceField(choices=VALID_MOVES),
            min_length=BOARD_SIZE,
            max_length=BOARD_SIZE,
            error_messages={
                'min_length': f"Each row must have exactly {BOARD_SIZE} columns.",
                'max_length': f"Each row must have exactly {BOARD_SIZE} columns.",
                'invalid_choice': f"Each cell must be one of: {', '.join(VALID_MOVES)}."
            }
        ),
        min_length=BOARD_SIZE,
        max_length=BOARD_SIZE,
        error_messages={
            'min_length': f"Board must have exactly {BOARD_SIZE} rows.",
            'max_length': f"Board must have exactly {BOARD_SIZE} rows.",
            'invalid': 'Board must be a 2D array.'
        }
    )

    class Meta:
        model = Game
        fields = ['uuid', 'createdAt', 'updatedAt', 'name', 'difficulty', 'gameState', 'board']

    def validate_name(self, value):
        """Validate game name format and content"""
        if not value:
            raise serializers.ValidationError("Game name cannot be empty.")
        if not re.match(r'^[\w\s-]+$', value):
            raise serializers.ValidationError("Game name can only contain letters, numbers, spaces, and hyphens.")
        return value

    def validate_uuid(self, value):
        """Validate UUID format and uniqueness"""
        if value:
            if not isinstance(value, uuid.UUID):
                try:
                    value = uuid.UUID(str(value))
                except ValueError:
                    raise serializers.ValidationError("Invalid UUID format.")
            
            if self.instance and self.instance.uuid != value:
                if Game.objects.filter(uuid=value).exists():
                    raise serializers.ValidationError("Game with this UUID already exists.")
        return value

    def validate_difficulty(self, value):
        """Validate difficulty choice"""
        value = str(value).lower()
        if value not in self.DIFFICULTY_CHOICES:
            raise serializers.ValidationError(
                "Invalid difficulty. Must be one of: easy, medium, hard."
            )
        return value

    def validate_gameState(self, value):
        """Validate game state"""
        value = str(value).lower()
        if value not in self.GAME_STATE_CHOICES:
            raise serializers.ValidationError(
                "Invalid game state. Must be one of: opening, midgame, endgame."
            )
        return value

    def validate_board(self, value):
        """Validate board dimensions and content"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Board must be a 2D array.")

        if len(value) != self.BOARD_SIZE:
            raise serializers.ValidationError(f"Board must have exactly {self.BOARD_SIZE} rows.")

        x_count = 0
        o_count = 0

        for row_idx, row in enumerate(value):
            if not isinstance(row, list):
                raise serializers.ValidationError(f"Row {row_idx + 1} must be a list.")
            
            if len(row) != self.BOARD_SIZE:
                raise serializers.ValidationError(f"Row {row_idx + 1} must have exactly {self.BOARD_SIZE} columns.")
            
            for col_idx, cell in enumerate(row):
                if cell == 'X':
                    x_count += 1
                elif cell == 'O':
                    o_count += 1
                elif cell != '':
                    raise serializers.ValidationError(f"Invalid move '{cell}' at position [{row_idx + 1}, {col_idx + 1}].")
        
        # Validate move counts
        if abs(x_count - o_count) > 1:
            raise serializers.ValidationError("Invalid move sequence: difference between X and O moves cannot exceed 1.")
        
        return value

    def validate(self, data):
        """Perform cross-field validation"""
        if data.get('gameState') == 'endgame':
            # Example additional validation for endgame state
            x_count = sum(row.count('X') for row in data.get('board', []))
            o_count = sum(row.count('O') for row in data.get('board', []))
            total_moves = x_count + o_count
            if total_moves < 30:
                raise serializers.ValidationError("Endgame state must have at least 30 moves.")
        return data

    def create(self, validated_data):
        """Handle creation with automatic timestamp and UUID"""
        if not validated_data.get('uuid'):
            validated_data['uuid'] = uuid.uuid4()
        validated_data['createdAt'] = timezone.now()
        validated_data['updatedAt'] = validated_data['createdAt']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Handle updates with automatic timestamp"""
        validated_data['updatedAt'] = timezone.now()
        return super().update(instance, validated_data)