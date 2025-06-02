import factory
from datetime import datetime
from factory import builder
from factory import utils

from accounts.factories import UserFactory
from .models import Website

class WebsiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Website

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "title%d" % n)
    url = factory.Sequence(lambda n: "https://wwww.test%d.com" % n)