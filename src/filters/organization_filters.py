import django_filters
from src.models import Organization


class OrganizationFilter(django_filters.FilterSet):

    class Meta:
        model = Organization
        exclude = ('main_image',)