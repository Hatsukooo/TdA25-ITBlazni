from django.db import models
from django.utils import timezone
import uuid

class Game(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10, default='easy')
    board = models.JSONField(default=list)
    game_state = models.CharField(max_length=50, default='initial')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
