from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response  
from rest_framework import status


class APIIndexView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': "OK"})