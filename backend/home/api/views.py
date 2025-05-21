from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view



class APIIndexView(APIView):
    pass


def index(request):
    return HttpResponse("ok")