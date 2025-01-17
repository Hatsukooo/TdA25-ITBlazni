from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def validate_board(self, value):
        if len(value) != 15 or any(len(row) != 15 for row in value):
            raise serializers.ValidationError("Board must be a 15x15 grid.")

        valid_symbols = {"X", "O", ""}
        for row in value:
            for cell in row:
                if cell not in valid_symbols:
                    raise serializers.ValidationError("Board contains invalid symbols.")

        x_count = sum(row.count("X") for row in value)
        o_count = sum(row.count("O") for row in value)
        if x_count < o_count or x_count > o_count + 1:
            raise serializers.ValidationError("Invalid starting player or symbol count.")

        return value
