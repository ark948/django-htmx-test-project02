from rest_framework.serializers import ModelSerializer, Serializer, IntegerField

from contacts.models import Contact

class ContactModelSerializer(ModelSerializer):
    class Meta:
        model = Contact
        exclude = [
            'id',
            'user'
        ]