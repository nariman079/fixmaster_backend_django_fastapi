# pylint: disable=no-member,too-few-public-methods
"""
Работа с организациями
"""

from django.db.models import Q

from rest_framework.response import Response

from src.models import OrganizationType, Organization, Service


def get_organization_types() -> Response:
    """
    Getting all organization types for filters on frontend
    """
    organization_types = OrganizationType.objects.filter().values("id", "title")
    return Response(
        {
            "message": "Данные успешно получены",
            "success": True,
            "data": organization_types,
        }
    )


def search_organization(search: str) -> Response:
    """
    Search organization by title and by organization type title
    """
    queryset = Organization.objects.filter(
        Q(title__icontains=search)
        | Q(organization_type__title__contains=search)
        | Q(organization_type__title__exact=search)
    ).values("id", "title")

    return Response(
        {"message": "Запрос успешно выполнен", "success": True, "data": queryset}
    )


def get_services_title() -> Response:
    """
    Get services lise for filters in frontend
    """
    queryset = Service.objects.values("id", "title")

    return Response(
        {"message": "Запрос успешно выполнен", "success": True, "data": queryset}
    )


def get_master_services(master_id: int) -> Response:
    """Get master services"""
    if master_id == 0:
        return Response(
            {"message": "Запрос успешно выполнен", "success": True, "data": []},
            status=200,
        )

    queryset = Service.objects.filter(master=master_id)
    return Response(
        {
            "message": "Запрос успешно выполнен",
            "success": True,
            "data": queryset.values(
                "id",
                "title",
                "short_description",
                "price",
                "min_time",
            ),
        },
        status=200,
    )
