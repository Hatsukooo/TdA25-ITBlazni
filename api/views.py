from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializer import GameSerializer
from .utils.logger import api_error_handler
import uuid

@api_error_handler
@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response({
                'message': 'Data retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if not serializer.validated_data.get('uuid'):
                    serializer.validated_data['uuid'] = uuid.uuid4()
                serializer.save()
                return Response({
                    'message': 'Game created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'message': 'Internal server error',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'message': 'Validation error',
            'errors': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_error_handler
@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request, pk):
    try:
        game = Game.objects.get(uuid=pk)
    except Game.DoesNotExist:
        return Response({
            "message": "Game not found."
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return Response({
            'message': 'Data retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Game updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Validation error',
            'errors': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        game.delete()
        return Response({
            'message': 'Game deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)

@api_error_handler
@api_view(['GET'])
def apicko(request):
    return Response({
        'organization': 'Student Cyber Games'
    }, status=status.HTTP_200_OK)