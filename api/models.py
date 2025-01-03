from django.db import models
from django.utils import timezone
import uuid

class Game(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    createdAt = models.DateTimeField(default=timezone.now, editable=False)
    updatedAt = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=False)
    difficulty = models.CharField(max_length=10, default='easy', blank=False)
    gameState = models.CharField(max_length=50, default='opening', blank=False)
    board = models.JSONField(default=list, blank=False)
    
    def __str__(self):
        return self.name