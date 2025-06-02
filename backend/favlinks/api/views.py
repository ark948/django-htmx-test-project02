from django.http.request import HttpRequest
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response



def api_index(request: HttpRequest) -> Response:
    return JsonResponse({'message': "API Index Ok."})