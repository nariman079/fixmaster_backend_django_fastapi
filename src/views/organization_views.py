from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from src.models import Organization
from src.serializers.organization_serializers import (OrganizationSerializer,
                                                      OrganizationDetailSerializer)


class OrganizationListView(APIView):
    """
    Controller for the organization's list page

    accessed methods: GET,
    """
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        try:
            organization_queryset = Organization.objects.filter(
                **self.request.query_params.dict()
            )
            organization_serializer = OrganizationSerializer(
                instance=organization_queryset,
                many=True,
                context={'request': self.request}
            )

            return Response(
                {
                    'message': "All organizations success received",
                    'success': True,
                    'data': organization_serializer.data
                }
            )
        except ValueError as ex:
            raise ValidationError(ex.args, code=400)


class OrganizationDetailView(APIView):
    """
    Controller for the detailed organization page

    accessed methods: GET,
    path param: organization_id
    """
    def get(self, request, organization_id: int, *args, **kwargs):
        try:
            organization = Organization.objects.get(id=organization_id)
            organization_serializer = OrganizationDetailSerializer(
                instance=organization,
                context={'request': self.request})

            return Response({
                'message': 'Organization detail success received',
                'success': True,
                'data': organization_serializer.data
                },
                status=200
            )
        except Organization.DoesNotExist:
            return Response(
                {
                    'message': "Such organization does not exist",
                    'success': False,
                    'data': []
                },
                status=404
            )