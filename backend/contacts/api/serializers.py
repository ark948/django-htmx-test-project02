from rest_framework.serializers import ModelSerializer, Serializer

from contacts.models import Contact

class ContactModelSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'