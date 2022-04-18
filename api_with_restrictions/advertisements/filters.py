from django_filters import rest_framework as filters
from rest_framework.authtoken.admin import User

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = filters.DateFromToRangeFilter()
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status']
