from typing import Any
from rest_framework.response import Response


class ErrorResponse(Response):

    def __init__(self, message: str, *args, **kwargs):
        data = {'error': message}
        super(ErrorResponse, self).__init__(data, *args, **kwargs)


class SuccessResponse(Response):

    def __init__(self, message: Any, *args, **kwargs):
        data = {'success': message}
        super(SuccessResponse, self).__init__(data, *args, **kwargs)
