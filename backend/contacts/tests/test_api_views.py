import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects
from django.db.models import QuerySet
from rest_framework.test import APIClient

from icecream import ic

from contacts.models import Contact
from contacts.api.views import (
    APIIndexView,
    ContactsListView
)



@pytest.mark.django_db
def test_contacts_api_index_view(user, client: APIClient):
    response = client.get(reverse("contacts:api_index"))
    
    assert response.status_code == 200
    assert response.data['message'] == "OK"
