import pytest
from django.test.client import Client
from django.urls import reverse


@pytest.mark.django_db
def test_home_index(client: Client):
    response = client.get(reverse("home:index"))
    assert response.status_code == 200