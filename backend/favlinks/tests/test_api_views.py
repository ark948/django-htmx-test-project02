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


@pytest.mark.django_db
def test_favlinks_api_websites_item_details(user, website_dict_params, client: APIClient):
    client.force_login(user)
    response = client.get(reverse("favlinks:api-website-item", kwargs={'pk': website_dict_params['id']}))

    assert response.status_code == 200
    assert response.data['id'] == website_dict_params['id']
    assert response.data['title'] == website_dict_params['title']
    assert response.data['url'] == website_dict_params['url']


@pytest.mark.django_db
def test_favlinks_api_websites_list_create_new(user, client: APIClient):
    client.force_login(user)
    response = client.get(reverse("favlinks:api-website-list"))

    assert response.status_code == 200
    assert response.data == []

    response = client.post(
        path=reverse('favlinks:api-website-list'),
        data={
            'title': 'MyWebsite',
            'url': 'https://www.some-website.com/'
        }
    )

    assert response.status_code == 201
    
    response = client.get(reverse("favlinks:api-website-list"))

    assert response.status_code == 200
    assert response.data != []
    assert len(response.data) == 1

    response = client.get(reverse("favlinks:api-website-item", kwargs={'pk': 1}))

    assert response.status_code == 200
    assert response.data['title'] == 'MyWebsite'
    assert response.data['url'] == 'https://www.some-website.com/'