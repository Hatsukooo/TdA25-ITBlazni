from rest_framework import serializers
from .models import Game
import uuid

class GameSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = Game
        fields = ['uuid', 'name', 'difficulty', 'board', 'game_state', 'created_at', 'updated_at']