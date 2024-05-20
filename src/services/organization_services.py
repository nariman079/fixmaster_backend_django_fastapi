from django.db.models import Q

from rest_framework.response import Response

from src.models import OrganizationType, Organization


def get_organization_types() -> Response:
    """
    Получения списка типов организаций
    """
    organization_types = OrganizationType.objects.filter().values('id', 'title')
    return Response({
        'message': "Данные успешно получены",
        'success': True,
        'data': organization_types
        }
    )


def search_organization(search: str) -> Response:

    queryset = Organization.objects.filter(
        Q(title__icontains=search) |
        Q(organization_type__title__contains=search) |
        Q(organization_type__title__exact=search)
    ).values('id', 'title')

    return Response(
        {
            'message': "Запрос успешно выполнен",
            'success': True,
            'data': queryset
        }
    )