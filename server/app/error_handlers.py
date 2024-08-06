from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .exceptions import BaseAPIException
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    # If this is a custom API exception, use its status code and message
    if isinstance(exc, BaseAPIException):
        response = Response({
            'error': exc.message,
            'status_code': exc.status_code
        }, status=exc.status_code)

    # If we don't have a response (i.e., the exception wasn't handled by DRF),
    # log it and return a generic error response
    if response is None:
        logger.error(f"Unhandled exception: {str(exc)}")
        response = Response({
            'error': 'An unexpected error occurred.',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response