from rest_framework import serializers

from favlinks.models import Website, Link, Category

class WebsiteDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = '__all__'

class WebsiteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        exclude = (
            'user',
        )


class LinkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = ( 'id' )