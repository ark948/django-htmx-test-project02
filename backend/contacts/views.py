from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from http import HTTPStatus

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "contacts/index.html", status=HTTPStatus.OK) # 200