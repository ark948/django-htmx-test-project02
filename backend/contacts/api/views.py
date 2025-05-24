from rest_framework.decorators import api_view
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from django.db.models import QuerySet

from . import serializers
from contacts.models import Contact


# testsed
class APIIndexView(views.APIView):
    def get(self, *args, **kwargs) -> Response:
        return Response({'message': "OK"})
    


# tested
class ContactsListView(generics.ListAPIView):
    permission_classes = ( permissions.IsAuthenticated, )
    serializer_class = serializers.ContactModelSerializer

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        qs: QuerySet = Contact.objects.filter(user = self.request.user)
        return qs
    


class ContactsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    serializer_class = serializers.ContactModelSerializer
    permission_classes = ( permissions.IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        queryset = Contact.objects.filter(user=request.user)
        serializer = serializers.ContactModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        qs: QuerySet = self.request.user.contacts.all()
        return qs