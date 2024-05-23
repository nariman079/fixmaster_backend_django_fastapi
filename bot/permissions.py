from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def api_key_permission(request) -> bool:
    api_key = request.headers.get('Api-Key')

    if api_key and api_key == 'test':
        return True
    else:
        return False
