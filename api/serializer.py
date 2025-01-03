from rest_framework import serializers
from .models import Game
import uuid

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['uuid','createdAt', 'updatedAt', 'name', 'difficulty', 'gameState', 'board' ]