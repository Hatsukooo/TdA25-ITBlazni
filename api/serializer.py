from rest_framework import serializers
from .models import Game
import uuid

class GameSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = Game
        fields = ['uuid','createdAt', 'updatedAt', 'name', 'difficulty', 'gameState', 'board' ]