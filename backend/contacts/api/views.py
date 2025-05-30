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
from . import permissions as custom_permissions
from contacts.models import Contact


# listCreateAPIView
# RetrieveUpdateDelete


# test ok
class APIIndexView(views.APIView):
    def get(self, *args, **kwargs) -> Response:
        return Response({'message': "OK"})
    

# test ok
class ContactsListView(generics.ListAPIView):
    permission_classes = ( permissions.IsAuthenticated, )
    serializer_class = serializers.ContactModelSerializer

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        qs: QuerySet = Contact.objects.filter( user = self.request.user )
        return qs
    

# test ok
class ContactDetailsView(generics.RetrieveAPIView):
    serializer_class = serializers.ContactDetailsSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custom_permissions.IsOwner
    )
    
    def get_queryset(self, *args, **kwargs) -> Contact:
        return Contact.objects.filter( user = self.request.user )
    


class NewContactView(generics.CreateAPIView):
    serializer_class = serializers.CreateNewContactSerializer
    permission_classes = ( permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'phone_number': request.data.get('phone_number'),
            'address': request.data.get('address')
        }

        serializer = serializers.CreateNewContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# in actuality, we may only need the following two generic views
class ConactsListCreateView(generics.ListCreateAPIView):
    pass

class ContactsDetailsUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    pass



# test ok
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