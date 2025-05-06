import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_contacts_index(client: Client):
    response = client.get(reverse("contacts:index"))

    assert response.status_code == 200
    assertTemplateUsed(response, "contacts/index.html")



@pytest.mark.django_db
def test_contacts_list_page(user, client: Client):
    client.force_login(user)

    response = client.get(reverse("contacts:list"))
    assert response.status_code == 200