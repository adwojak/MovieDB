from rest_framework.status import HTTP_400_BAD_REQUEST
from libs.errors import DEFAULT_ERROR
from libs.response import ErrorResponse


class OmdbApiError(Exception):
    pass


class MovieDoesNotExist(Exception):
    pass


class BadDataFormat(Exception):
    pass


def exception_handler(exception, context):
    status = HTTP_400_BAD_REQUEST
    if hasattr(exception, 'args') and len(exception.args) > 0:
        exception_message = exception.args[0]
    elif hasattr(exception, 'detail'):
        if hasattr(exception, 'status_code'):
            status = exception.status_code
        exception_message = str(exception.detail)
    else:
        exception_message = DEFAULT_ERROR
    return ErrorResponse(exception_message, status=status)
