from rest_framework import serializers
from .models import Game
import uuid

class GameSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=False)

    class Meta:
        model = Game
        fields = ['uuid', 'createdAt', 'updatedAt', 'name', 'difficulty', 'gameState', 'board']
        read_only_fields = ['uuid', 'createdAt', 'updatedAt']