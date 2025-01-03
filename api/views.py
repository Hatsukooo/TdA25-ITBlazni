from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializer import GameSerializer
from .exceptions import GameNotFoundError, ValidationError, DatabaseError
from .constants import ERROR_MESSAGES, ERROR_CODES
from .utils.logger import api_error_handler
import uuid

@api_view(['GET', 'POST'])
@api_error_handler
def game_list(request):
    if request.method == 'GET':
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response({'message': 'Data retrieved successfully', 'data': serializer.data}, 
                          status=status.HTTP_200_OK)
        except Exception as e:
            raise DatabaseError(detail=ERROR_MESSAGES['DATABASE_ERROR'])

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        try:
            if not serializer.validated_data.get('uuid'):
                serializer.validated_data['uuid'] = uuid.uuid4()
            serializer.save()
            return Response({'message': 'Game created successfully', 'data': serializer.data}, 
                          status=status.HTTP_201_CREATED)
        except Exception as e:
            raise DatabaseError(detail=ERROR_MESSAGES['DATABASE_ERROR'])

@api_view(['GET', 'PUT', 'DELETE'])
@api_error_handler
def game_detail(request, pk):
    try:
        game = Game.objects.get(uuid=pk)
    except Game.DoesNotExist:
        raise GameNotFoundError(detail=ERROR_MESSAGES['GAME_NOT_FOUND'])

    if request.method == 'GET':
        try:
            serializer = GameSerializer(game)
            return Response({'message': 'Data retrieved successfully', 'data': serializer.data}, 
                          status=status.HTTP_200_OK)
        except Exception as e:
            raise DatabaseError(detail=ERROR_MESSAGES['DATABASE_ERROR'])

    elif request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        try:
            serializer.save()
            return Response({'message': 'Game updated successfully', 'data': serializer.data}, 
                          status=status.HTTP_200_OK)
        except Exception as e:
            raise DatabaseError(detail=ERROR_MESSAGES['DATABASE_ERROR'])

    elif request.method == 'DELETE':
        try:
            game.delete()
            return Response({'message': 'Game deleted successfully'}, 
                          status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise DatabaseError(detail=ERROR_MESSAGES['DATABASE_ERROR'])

@api_view(['GET'])
@api_error_handler
def apicko(request):
    return Response({'organization': 'Student Cyber Games'}, status=status.HTTP_200_OK)