import django_filters

from .models import Contact


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        field_name='first_name', lookup_expr="icontains"
    )

    last_name = django_filters.CharFilter(
        field_name='last_name', lookup_expr="icontains"
    )

    email = django_filters.CharFilter(
        field_name='email', lookup_expr='icontains'
    )

    phone_number = django_filters.NumberFilter(
        field_name='phone_number', lookup_expr='icontains'
    )

    created_at = django_filters.DateFilter(
        field_name='created_at'
    )

    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'email', 'phone_number', 'address', 'created_at'
        )