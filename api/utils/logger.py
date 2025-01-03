import logging
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException

logger = logging.getLogger(__name__)

def api_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in {func.__name__}: {str(e)}")
            return Response({
                'message': 'Validation error',
                'errors': e.detail
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except APIException as e:
            logger.error(f"API exception in {func.__name__}: {str(e)}")
            return Response({
                'message': e.default_detail,
                'error': str(e),
                'code': e.default_code
            }, status=e.status_code)
        except Exception as e:
            logger.error(f"Unhandled exception in {func.__name__}: {str(e)}")
            return Response({
                'message': 'Internal server error',
                'error': str(e),
                'code': 'internal_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper