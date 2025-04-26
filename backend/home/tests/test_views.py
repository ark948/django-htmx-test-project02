import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_home_index(client: Client):
    response = client.get(reverse("home:index"))
    assert response.status_code == 200
    assertTemplateUsed(response, "home/index.html")