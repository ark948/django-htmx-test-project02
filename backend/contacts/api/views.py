from rest_framework.decorators import api_view
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import HttpRequest
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
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

    def list(self, request: HttpRequest, *args, **kwargs) -> Response:
        queryset: QuerySet = Contact.objects.filter(user=request.user)
        serializer = serializers.ContactModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # this method handles POST, returns 201
    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(user = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # this may be unnecessary, not sure yet
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        qs: QuerySet = self.request.user.contacts.all()
        return qs