import pytest


from contacts.models import Contact


@pytest.mark.django_db
def test_contact_model_full_name(user, contact_dict_params):
    contact_item = user.contacts.all()[0]

    assert contact_item.first_name == contact_dict_params['first_name']
    assert contact_item.last_name == contact_dict_params['last_name']
    assert contact_item.email == contact_dict_params['email']
    assert contact_item.phone_number == contact_dict_params['phone_number']