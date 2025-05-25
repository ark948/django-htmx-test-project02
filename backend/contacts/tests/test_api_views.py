import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects
from django.db.models import QuerySet
from rest_framework.test import (
    APIClient,
    APIRequestFactory,
    force_authenticate
)

from icecream import ic

from accounts.models import CustomUser
from contacts.models import Contact
from contacts.api.views import (
    APIIndexView,
    ContactsListView,
    ContactsViewSet
)



@pytest.mark.django_db
def test_contacts_api_index_view(user, client: APIClient):
    response = client.get(reverse("contacts:api_index"))
    
    assert response.status_code == 200
    assert response.data['message'] == "OK"



@pytest.mark.django_db
def test_contacts_api_contacts_list_view(user, user_contacts, client: APIClient):
    client.force_login(user)
    resposne = client.get(reverse("contacts:api_list"))

    assert resposne.status_code == 200
    assert len(resposne.data) == 5
    assert resposne.data[0]['first_name'] == user_contacts[0].first_name



@pytest.mark.django_db
def test_contacts_api_contacts_viewset( user, user_contacts ):
    factory = APIRequestFactory()
    request = factory.get("/contacts/api/set/list/")
    force_authenticate(request, user)
    view = ContactsViewSet.as_view({'get': 'list'})
    response = view(request)
    
    assert response.status_code == 200
    assert len(response.data) == 5
    assert response.data[0]['first_name'] == user_contacts[0].first_name
    assert response.data[1]['last_name'] == user_contacts[1].last_name
    assert response.data[2]['email'] == user_contacts[2].email
    assert response.data[3]['phone_number'] == user_contacts[3].phone_number
