from django.db import models
from django.utils import timezone
import uuid

class Game(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=False)
    difficulty = models.CharField(max_length=10, default='easy', blank=False)
    board = models.JSONField(default=list, blank=False)
    game_state = models.CharField(max_length=50, default='opening', blank=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name