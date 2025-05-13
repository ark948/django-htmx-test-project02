import django_filters
import django_filters.fields
from django import forms

from .models import Contact


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter( field_name='first_name', lookup_expr="icontains" )
    last_name = django_filters.CharFilter( field_name='last_name', lookup_expr="icontains" )
    # encrypted fields may not work

    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name',
        )