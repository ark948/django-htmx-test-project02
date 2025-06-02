import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_favlinks_api_index(client: APIClient):
    response = client.get(reverse("favlinks:api-index"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_favlinks_api_websites_list_is_empty(user, client: APIClient):
    client.force_login(user)
    response = client.get(reverse("favlinks:api-website-list"))

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_favlinks_api_websites_list_not_empty(user, user_with_one_website, client: APIClient):
    client.force_login(user)
    response = client.get(reverse("favlinks:api-website-list"))

    assert response.status_code == 200
    assert response.data != []
    assert response.data[0]['title'] == user_with_one_website.title
    assert response.data[0]['url'] == user_with_one_website.url
    assert len(response.data) == 1


@pytest.mark.django_db
def test_favlinks_api_websites_mulitple_objects(user, user_websites, client: APIClient):
    client.force_login(user)
    response = client.get(reverse("favlinks:api-website-list"))

    assert response.status_code == 200
    assert response.data != []
    assert len(response.data) == 3
    assert response.data[0]['title'] == user_websites[0].title
    assert response.data[1]['url'] == user_websites[1].url