import pytest

from accounts.factories import UserFactory
from favlinks.factories import WebsiteFactory
from favlinks.models import Website

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def user_with_one_website(user):
    website = Website.objects.create(
        title = "Youtube",
        url = "https://www.youtube.com/",
        user = user
    )
    website.save()
    return website

@pytest.fixture
def user_websites(user):
    return WebsiteFactory.create_batch(3, user=user)

@pytest.fixture
def website_dict_params(user):
    website = WebsiteFactory.create(user=user)
    return website.__dict__