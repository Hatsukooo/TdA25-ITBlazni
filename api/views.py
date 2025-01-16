from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from .models import Game
from .serializers import GameSerializer
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Debug prints (optional):
        print("POST request received for game detail")
        print(f"Received POST data: {request.data}")  

        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Validate board layout
                board = serializer.validated_data.get('board')
                if len(board) != 15:
                    return Response(
                        {"code": 422, "message": "Semantic error: Board must have exactly 15 rows."},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )
                for row_index, row in enumerate(board):
                    if len(row) != 15:
                        return Response(
                            {"code": 422, "message": f"Semantic error: Row {row_index + 1} must have exactly 15 cells."},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY
                        )

                # Validate symbols
                valid_characters = ['', 'X', 'O']
                invalid_cells = []
                for row_index, row in enumerate(board):
                    for col_index, cell in enumerate(row):
                        if cell not in valid_characters:
                            invalid_cells.append(f"Row {row_index + 1}, Col {col_index + 1} has invalid value '{cell}'")
                if invalid_cells:
                    return Response(
                        {"code": 422, "message": f"Semantic error: Invalid characters found: {', '.join(invalid_cells)}. "
                                                 f"Only allowed characters: {', '.join(valid_characters)}."},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )

                # Validate X/O counts (starting player check)
                xCount = sum(row.count('X') for row in board)
                oCount = sum(row.count('O') for row in board)
                if xCount < oCount or xCount > oCount + 1:
                    return Response(
                        {"code": 422, "message": "Invalid starting player or symbol count."},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )

                # Validate user-supplied gameState if present
                allowed_states = ['opening', 'midgame', 'endgame', 'finished']
                posted_state = serializer.validated_data.get('gameState', 'opening')
                if posted_state not in allowed_states:
                    return Response(
                        {"code": 422, "message": f"Invalid gameState: {posted_state}"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )

                # Save the game with the user-supplied or default gameState
                serializer.save(gameState=posted_state)

                # Debug print
                print(f"Saved game data: {serializer.data}")  
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"Semantic error: {str(e)}")
                return Response(
                    {"code": 422, "message": f"Semantic error: {str(e)}"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

        # If serializer is not valid
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request, pk):
    try:
        game = Game.objects.get(uuid=pk)
    except Game.DoesNotExist:
        return Response({"code": 404, "message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return Response(serializer.data)


    elif request.method == 'PUT':
        print("PUT request received for game detail")
        serializer = GameSerializer(game, data=request.data)
        print("SERIALIZER LOAD")
        
        if serializer.is_valid():
            print("SERIALIZER VALID CHECK")
            try:
                board = serializer.validated_data.get('board')

                if len(board) != 15:
                    print("Board must have exactly 15 rows.")
                    return Response({"code": 422, "message": "Semantic error: Board must have exactly 15 rows."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                

                for row_index, row in enumerate(board):
                    if len(row) != 15:
                        print(f"Row {row_index + 1} does not have exactly 15 cells.")
                        return Response({"code": 422, "message": f"Semantic error: Row {row_index + 1} must have exactly 15 cells."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                valid_characters = ['', 'X', 'O']
                invalid_cells = []
                for row_index, row in enumerate(board):
                    for col_index, cell in enumerate(row):
                        if cell not in valid_characters:
                            invalid_cells.append(f"Row {row_index + 1}, Col {col_index + 1} has invalid value '{cell}'")

                if invalid_cells:
                    print(f"Invalid characters found: {invalid_cells}")
                    return Response({"code": 422, "message": f"Semantic error: Invalid characters found: {', '.join(invalid_cells)}. Only allowed characters: {', '.join(valid_characters)}."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                serializer.save()
                print("Game updated successfully")
                return Response(serializer.data)

            except Exception as e:
                print(f"Semantic error: {str(e)}")
                return Response({"code": 422, "message": f"Semantic error: {str(e)}"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        print(f"Bad request: {serializer.errors}")
        return Response({"code": 400, "message": f"Bad request: {serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'DELETE':
        print("DELETE request received for game detail")
        game.delete()
        print("Game deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def apicko(request):
    return JsonResponse({"organization": "Student Cyber Games"})

