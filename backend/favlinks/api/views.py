from django.db.models import QuerySet
from django.http.request import HttpRequest
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from . import serializers
from favlinks.models import Website


def api_index(request: HttpRequest) -> Response:
    return JsonResponse({'message': "API Index Ok."})


# listCreateAPIView
# RetrieveUpdateDelete


class WebsiteView(generics.ListCreateAPIView):
    serializer_class = serializers.WebsiteModelSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        return Website.objects.filter( user = self.request.user )
    
    def post(self, request: HttpRequest, *args, **kwargs):
        data = {
            'title' : request.data.get('title'),
            'url': request.data.get('url'),
            'username': request.data.get('username'),
            'password': request.data.get('password'),
        }

        serializer = serializers.WebsiteModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)