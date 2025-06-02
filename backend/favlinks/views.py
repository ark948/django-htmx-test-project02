from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Ok")