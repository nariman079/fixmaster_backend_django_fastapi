# pylint: disable=missing-class-docstring
"""
Views for organization
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from src.models import Organization
from src.serializers.organization_serializers import (
    OrganizationSerializer,
    OrganizationDetailSerializer,
)
from src.services.organization_services import (
    get_organization_types,
    search_organization,
    get_services_title,
    get_master_services,
)


class OrganizationListView(APIView):
    """
    Controller for the organization's list page

    accessed methods: GET,
    """

    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        """Получение списка организаций"""
        try:
            organization_queryset = Organization.objects.filter(
                **self.request.query_params.dict()
            ).filter(is_verified=True)
            organization_serializer = OrganizationSerializer(
                instance=organization_queryset,
                many=True,
                context={"request": self.request},
            )

            return Response(
                {
                    "message": "All organizations success received",
                    "success": True,
                    "data": organization_serializer.data,
                }
            )
        except ValueError as ex:
            raise ValidationError(ex.args, code=400) from ex


class OrganizationDetailView(APIView):
    """
    Controller for the detailed organization page

    accessed methods: GET,
    path param: organization_id
    """

    def get(self, request, organization_id: int, *args, **kwargs):
        """Получение детальной информации"""
        try:
            organization = Organization.objects.get(id=organization_id)
            organization_serializer = OrganizationDetailSerializer(
                instance=organization, context={"request": self.request}
            )

            return Response(
                {
                    "message": "Organization detail success received",
                    "success": True,
                    "data": organization_serializer.data,
                },
                status=200,
            )
        except Organization.DoesNotExist:
            return Response(
                {
                    "message": "Such organization does not exist",
                    "success": False,
                    "data": [],
                },
                status=404,
            )


class OrganizationTypeListView(APIView):
    def get(self, *args, **kwargs):
        """Получение списка типов организаций"""
        return get_organization_types()


class ServiceListView(APIView):
    """
    Controller for services list
    """

    def get(self, *args, **kwargs):
        """Получение списка услуг"""
        return get_services_title()


class SearchOrganization(APIView):
    @extend_schema(
        description="Search organization",
        methods=["GET"],
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search text",
            ),
        ],
    )
    def get(self, *args, **kwargs):
        """
        search: query params from url ".../organization/?search="
        search: string
        """
        if text := self.request.query_params.get("search"):
            return search_organization(text)

        return Response(
            {"message": "Запрос успешно выполнен", "success": True, "data": []}
        )


class MasterListView(APIView):
    def get(self, *args, **kwargs) -> Response:
        """Получаем все услуги мастера"""
        return get_master_services(self.request.query_params.get("master_id", 0))
