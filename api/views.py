from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import GameSerializer
from .utils.game_logic import classify_game_state
from django.http import JsonResponse

@api_view(['POST'])
def game_list(request):
    if request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.validated_data['board']
            
            # Classify the game state
            game_state = classify_game_state(board)
            serializer.save(gameState=game_state)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['PUT'])
def game_detail(request, pk):
    try:
        game = Game.objects.get(uuid=pk)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            board = serializer.validated_data['board']
            
            # Classify the game state
            game_state = classify_game_state(board)
            serializer.save(gameState=game_state)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    
@api_view(['GET'])
def apicko(request):
    return JsonResponse({"organization": "Student Cyber Games"})

