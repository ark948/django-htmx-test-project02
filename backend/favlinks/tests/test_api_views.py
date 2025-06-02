import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_favlinks_api_index(client: APIClient):
    response = client.get(reverse("favlinks:api-index"))

    assert response.status_code == 200