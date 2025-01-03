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
    NAME_MAX_LENGTH = 100

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
        max_length=NAME_MAX_LENGTH,
        error_messages={
            'required': 'Game name is required.',
            'blank': 'Game name cannot be blank.',
            'max_length': f'Game name cannot exceed {NAME_MAX_LENGTH} characters.',
            'invalid': 'Game name contains invalid characters.'
        }
    )
    difficulty = serializers.CharField(
        error_messages={
            'required': 'Difficulty level is required.',
            'invalid_choice': f'Difficulty must be one of: {", ".join(DIFFICULTY_CHOICES)}'
        }
    )
    gameState = serializers.CharField(
        error_messages={
            'required': 'Game state is required.',
            'invalid_choice': f'Game state must be one of: {", ".join(GAME_STATE_CHOICES)}'
        }
    )
    board = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField(max_length=1, allow_blank=True),
            min_length=BOARD_SIZE,
            max_length=BOARD_SIZE,
        ),
        min_length=BOARD_SIZE,
        max_length=BOARD_SIZE,
        error_messages={
            'required': 'Game board is required.',
            'invalid': 'Invalid board format.',
            'min_length': f'Board must be {BOARD_SIZE}x{BOARD_SIZE}.',
            'max_length': f'Board must be {BOARD_SIZE}x{BOARD_SIZE}.'
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
                f"Invalid difficulty. Must be one of: {', '.join(self.DIFFICULTY_CHOICES)}"
            )
        return value

    def validate_gameState(self, value):
        """Validate game state"""
        value = str(value).lower()
        if value not in self.GAME_STATE_CHOICES:
            raise serializers.ValidationError(
                f"Invalid game state. Must be one of: {', '.join(self.GAME_STATE_CHOICES)}"
            )
        return value

    def validate_board(self, value):
        """Validate board dimensions and content"""
        if not isinstance(value, list):
            raise serializers.ValidationError({
                'board': "Board must be a 2D array"
            })
        
        if len(value) != self.BOARD_SIZE:
            raise serializers.ValidationError({
                'board': f"Board must have exactly {self.BOARD_SIZE} rows"
            })

        x_count = 0
        o_count = 0
        
        for row_idx, row in enumerate(value):
            if not isinstance(row, list):
                raise serializers.ValidationError({
                    'board': f"Row {row_idx + 1} must be a list"
                })
                
            if len(row) != self.BOARD_SIZE:
                raise serializers.ValidationError({
                    'board': f"Row {row_idx + 1} must have exactly {self.BOARD_SIZE} columns"
                })
                
            for col_idx, cell in enumerate(row):
                if not isinstance(cell, str):
                    raise serializers.ValidationError({
                        'board': f"Cell at position [{row_idx + 1}, {col_idx + 1}] must be a string"
                    })
                    
                if cell not in self.VALID_MOVES:
                    raise serializers.ValidationError({
                        'board': f"Invalid move '{cell}' at position [{row_idx + 1}, {col_idx + 1}]"
                    })
                    
                if cell == 'X':
                    x_count += 1
                elif cell == 'O':
                    o_count += 1

        # Validate move counts
        if abs(x_count - o_count) > 1:
            raise serializers.ValidationError({
                'board': "Invalid number of moves. The difference between X and O moves cannot exceed 1."
            })

        return value

    def validate(self, data):
        """Perform cross-field validation"""
        if data.get('gameState') == 'endgame':
            # Additional endgame state validation logic here
            pass
            
        return data

    def create(self, validated_data):
        """Handle creation with automatic timestamp"""
        if not validated_data.get('uuid'):
            validated_data['uuid'] = uuid.uuid4()
        validated_data['createdAt'] = timezone.now()
        validated_data['updatedAt'] = validated_data['createdAt']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Handle updates with automatic timestamp"""
        validated_data['updatedAt'] = timezone.now()
        return super().update(instance, validated_data)