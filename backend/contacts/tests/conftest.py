import pytest


from accounts.factories import UserFactory
from contacts.factories import ContactFactory


@pytest.fixture
def user():
    return UserFactory()



@pytest.fixture
def user_contacts(user):
    return ContactFactory.create_batch(5, user=user)


@pytest.fixture
def contact_dict_params(user):
    contact = ContactFactory.create(user=user)
    return {
        'first_name': contact.first_name,
        'last_name': contact.last_name
    }