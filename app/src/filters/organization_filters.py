"""
Классы фильтров
"""

import django_filters
from src.models import Organization


# pylint: disable=too-few-public-methods,missing-class-docstring
class OrganizationFilter(django_filters.FilterSet):
    """Фильтры для организаций"""

    class Meta:
        model = Organization
        exclude = ("main_image",)
