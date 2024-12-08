from django.db import models
import json

class Game(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, default='easy')
    board = models.JSONField(default=list)

    def __str__(self):
        return self.name
