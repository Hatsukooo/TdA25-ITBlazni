from rest_framework.exceptions import APIException
from rest_framework import status

class GameNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Game not found'
    default_code = 'game_not_found'

class ValidationError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Invalid data'
    default_code = 'validation_error'

class DatabaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Database error'
    default_code = 'database_error'