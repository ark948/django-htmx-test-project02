from rest_framework.serializers import ModelSerializer, Serializer, IntegerField

from contacts.models import Contact

class ContactModelSerializer(ModelSerializer):
    class Meta:
        model = Contact
        exclude = (
            'id',
            'user'
        )



class ContactDetailsSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'



class CreateNewContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        exclude = (
            'id',
            'created_at',
            'user',
        )