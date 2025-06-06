from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# Create your views here.

# test ok
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "favlinks/index.html")

def create_new_website(request: HttpRequest) -> HttpResponse:
    return render(request, "favlinks/new.html", {})