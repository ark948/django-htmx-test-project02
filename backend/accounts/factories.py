import factory
from datetime import datetime


from .models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.CustomUser'
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: 'user%d' % n)