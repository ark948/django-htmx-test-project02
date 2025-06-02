import pytest
from django.test.client import Client
from django.urls import reverse


@pytest.mark.django_db
def test_favlinks_index(client: Client):
    response = client.get(reverse("favlinks:index"))

    assert response.status_code == 200