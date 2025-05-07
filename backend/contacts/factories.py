import factory
from datetime import datetime

import factory.builder
import factory.utils


from accounts.factories import UserFactory
from .models import Contact



class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    user = factory.SubFactory(UserFactory)
    first_name = 'hello'
    last_name = 'world'
    email = factory.Sequence(lambda n: 'user%d@gmail.com' % n)
    phone_number = str(factory.Sequence(lambda n: n))