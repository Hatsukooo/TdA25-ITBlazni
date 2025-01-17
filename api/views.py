from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import NotFound
import logging

from .models import Game
from .serializers import GameSerializer
from .utils.game_logic import classify_game_state

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def game_list(request):
    """
    Retrieve all games (optionally filtered by query params) or create a new game.
    """

    if request.method == 'GET':
        games = Game.objects.all()

        # Grab query params
        name = request.GET.get('name', '').strip()
        difficulty = request.GET.get('difficulty', '').strip()
        updated = request.GET.get('updated', '').strip()

        # Filter by name (partial match, case-insensitive)
        if name:
            games = games.filter(name__icontains=name)
        
        # Filter by difficulty (exact match, ignoring case)
        if difficulty:
            games = games.filter(difficulty__iexact=difficulty)
        
        # Filter by last updated: 24h, 7d, 1m, 3m
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        if updated == '24h':
            threshold = now - timedelta(hours=24)
            games = games.filter(updatedAt__gte=threshold)
        elif updated == '7d':
            threshold = now - timedelta(days=7)
            games = games.filter(updatedAt__gte=threshold)
        elif updated == '1m':
            threshold = now - timedelta(days=30)
            games = games.filter(updatedAt__gte=threshold)
        elif updated == '3m':
            threshold = now - timedelta(days=90)
            games = games.filter(updatedAt__gte=threshold)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Existing create logic stays the same
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.validated_data['board']
            game_state = classify_game_state(board)
            logger.debug(f"Classified game state: {game_state}")
            serializer.save(gameState=game_state)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f"Validation error during game creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request, pk):
    """
    Retrieve, update, or delete a specific game.
    """
    # Unchanged
    game = get_object_or_404(Game, uuid=pk)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            board = serializer.validated_data['board']
            game_state = classify_game_state(board)
            logger.debug(f"Updated game state: {game_state}")
            serializer.save(gameState=game_state)
            return Response(serializer.data)

        logger.error(f"Validation error during game update: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        game.delete()
        logger.info(f"Deleted game with UUID: {pk}")
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def apicko(request):
    """
    Basic static endpoint for testing.
    """
    logger.debug("apicko endpoint accessed.")
    return Response({"organization": "Student Cyber Games"})
