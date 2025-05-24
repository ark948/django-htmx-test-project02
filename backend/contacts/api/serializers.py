from rest_framework.serializers import ModelSerializer, Serializer


class ContactModelSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'