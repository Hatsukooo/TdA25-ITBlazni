from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['uuid', 'createdAt', 'updatedAt', 'name', 'difficulty', 'gameState', 'board']
        read_only_fields = ['uuid', 'createdAt', 'updatedAt']

    def validate_board(self, board):
        if len(board) != 15 or any(len(row) != 15 for row in board):
            raise serializers.ValidationError("Board must be a 15x15 grid.")
        
        valid_symbols = {'', 'X', 'O'}
        for row in board:
            if not all(cell in valid_symbols for cell in row):
                raise serializers.ValidationError("Board contains invalid symbols.")
        
        x_count = sum(row.count('X') for row in board)
        o_count = sum(row.count('O') for row in board)
        if x_count < o_count or x_count > o_count + 1:
            raise serializers.ValidationError("Invalid starting player or symbol count.")
        
        return board
