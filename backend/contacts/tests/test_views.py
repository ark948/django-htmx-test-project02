import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects
from django.db.models import QuerySet

from contacts.models import Contact


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
    assertTemplateUsed(response, "contacts/contacts-list.html")



@pytest.mark.django_db
def test_contacts_list_page_context_exists(user, user_contacts, client: Client):
    client.force_login(user)

    response = client.get(reverse("contacts:list"))
    assert 'contacts' in response.context
    assert type(response.context['contacts']) == QuerySet
    assert list(response.context['contacts']) == user_contacts



@pytest.mark.django_db
def test_contacts_list_page_without_login_redirects_to_login(user, client: Client):
    response = client.get(reverse("contacts:list"), follow=True)

    assertRedirects(response, '/accounts/login/?next=%2Fcontacts%2Flist%2F')
    


@pytest.mark.django_db
def test_contacts_list_page_context_is_appropriate(user, user_contacts, client: Client):
    client.force_login(user)
    response = client.get(reverse("contacts:list"))

    assert response.status_code == 200
    assert type(response.context['contacts'][0]) == type(user_contacts[0])
    assert response.context['contacts'][0] == user_contacts[0]
    assert type(response.context['contacts'][0]) == Contact