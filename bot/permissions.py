from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


def api_key_permission(request) -> None:
        api_key = request.META.get('Api-Key')
        if not (api_key and api_key == 'test'):
            raise ValidationError(
                {
                    'message': "Не верный Api-Key",
                    'success': True,
                    'data':[]
                }
            )
