import pytest


from accounts.factories import UserFactory
from contacts.factories import ContactFactory
from contacts.models import Contact


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def user_one_item(user):
    item = Contact.objects.create(
        first_name = 'John',
        last_name = 'Doe',
        email = "johndoe@gmail.com",
        phone_number = '111000222',
        address = 'New York, USA',
        user=user
    )
    item.save()
    return item


@pytest.fixture
def user_contacts(user):
    return ContactFactory.create_batch(5, user=user)


@pytest.fixture
def contact_dict_params(user):
    contact = ContactFactory.create(user=user)
    return {
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'email': contact.email,
        'phone_number': contact.phone_number,
        'address': contact.address,
        'created_at': contact.created_at,
        'user': contact.user
    }