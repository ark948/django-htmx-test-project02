import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects
from django.db.models import QuerySet

from contacts.models import Contact
from contacts.forms import ContactItemEditForm
from contacts.managers import ContactModelCustomQuerySet


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
    assert 'filter' in response.context
    assert type(response.context['filter'].qs) == ContactModelCustomQuerySet
    assert list(response.context['filter'].qs) == user_contacts



@pytest.mark.django_db
def test_contacts_list_page_without_login_redirects_to_login(user, client: Client):
    response = client.get(reverse("contacts:list"), follow=True)

    assertRedirects(response, '/accounts/login/?next=%2Fcontacts%2Flist%2F')
    


@pytest.mark.django_db
def test_contacts_list_page_context_is_appropriate(user, user_contacts, client: Client):
    client.force_login(user)
    response = client.get(reverse("contacts:list"))

    assert response.status_code == 200
    assert type(response.context['filter'].qs[0]) == type(user_contacts[0])
    assert response.context['filter'].qs[0] == user_contacts[0]
    assert type(response.context['filter'].qs[0]) == Contact



@pytest.mark.django_db
def test_contacts_list_from_neapolitan_is_protected(user, user_contacts, client: Client):
    response = client.get('/contacts/contact/', follow=True)
    assertRedirects(response, '/accounts/login/?next=%2Fcontacts%2Fcontact%2F')


@pytest.mark.django_db
def test_contacts_list_from_neapolitan_is_accessible_through_login(user, user_contacts, client: Client):
    client.force_login(user)
    response = client.get('/contacts/contact/')
    
    assert response.status_code == 200



@pytest.mark.django_db
def test_contacts_contact_item_view(user, user_contacts, client: Client):
    client.force_login(user)
    response = client.get(reverse("contacts:item-detail", kwargs={'pk': 1}))

    assert response.status_code == 200
    assertTemplateUsed(response, "contacts/partials/item-data/item.html")
    assert response.context['item'] == user_contacts[0]
    item_a = response.context['item']
    item_b = user_contacts[0]
    assert item_a.id == item_b.id
    assert item_a.first_name == item_b.first_name
    assert item_a.last_name == item_b.last_name
    assert item_a.full_name == item_b.full_name
    assert item_a.email == item_b.email
    assert item_a.phone_number == item_b.phone_number
    assert item_a.address == item_b.address
    assert item_a.created_at == item_b.created_at

    assert type(response.context['item']) == Contact



@pytest.mark.skip
def test_contacts_contact_edit(user, user_one_item, client: Client):
    client.force_login(user)
    
    # CHECKING ITEM BEFORE
    item = client.get( reverse('contacts:item-detail', kwargs={'pk': user_one_item.pk}) ).context['item']
    print(item.first_name)

    # ATTEMPTING TO UPDATE
    response = client.post( reverse("contacts:item-edit", kwargs={"pk": user_one_item.pk}), {"first_name": "shit"},
            headers = {'HTTP_HX-Request': 'true'}
        )
    assert response.status_code == 200

    # CHECKING ITEM AFTER
    item = client.get( reverse('contacts:item-detail', kwargs={'pk': user_one_item.pk}) ).context['item']
    print(item.first_name)



# This is very weird
@pytest.mark.django_db
def test_contacts_contact_edit(user, user_one_item, client: Client):
    client.force_login(user)
    
    # CHECKING ITEM BEFORE
    item = client.get( reverse('contacts:item-detail', kwargs={'pk': user_one_item.pk}) ).context['item']
    assert user_one_item.first_name == "John"

    # ATTEMPTING TO UPDATE
    response = client.post( 
            reverse("contacts:edit", kwargs={"pk": user_one_item.pk}),
            data={
                "first_name": "Bob",
                "phone_number": user_one_item.phone_number
            },
            headers = {'HTTP_HX-Request': 'true'}
        )
    
    # CHECKING ITEM AFTER
    item: Contact = client.get( reverse('contacts:item-detail', kwargs={'pk': user_one_item.pk}) ).context['item']
    assert item.first_name == "Bob"
    assert item.first_name != "John"



@pytest.mark.django_db
def test_contacts_contact_delete(user, user_contacts, client: Client):
    client.force_login(user)

    contacts = user.contacts.all()
    assert len(contacts) == 5

    response = client.delete( path=reverse("contacts:delete", kwargs={"pk": 5}), follow=True )
    contacts = user.contacts.all()
    assert len(contacts) == 4

    response = client.delete( path=reverse("contacts:delete", kwargs={"pk": 4}), follow=True )
    contacts = user.contacts.all()
    assert len(contacts) == 3


@pytest.mark.django_db
def test_contacts_new_contact_item(user, client: Client):
    contacts = user.contacts.all()
    assert len(contacts) == 0

    client.force_login(user)
    response = client.post(
        path=reverse('contacts:new'),
        data = {
            'first_name': "some_first_name",
            'phone_number': "111000222"
        },
        headers = {'HTTP_HX-Request': 'true'}
    )

    assert response.status_code == 202
    contacts = user.contacts.all()
    assert len(contacts) == 1