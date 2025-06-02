from rest_framework import serializers

from favlinks.models import Website, Link, Category

class WebsiteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        exclude = (
            'id',
            'user',
        )


class LinkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = ( 'id' )