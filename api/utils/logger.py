from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def api_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return Response({
                'message': 'Internal server error',
                'error': str(e),
                'code': getattr(e, 'default_code', 'internal_error')
            }, status=getattr(e, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR))
    return wrapper