from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from rest_framework import permissions
from django.db.models import QuerySet

from . import serializers
from contacts.models import Contact


class APIIndexView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': "OK"})
    


class ContactsListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ContactModelSerializer

    def get_queryset(self, *args, **kwargs):
        qs = Contact.objects.filter(user = self.request.user)
        return qs