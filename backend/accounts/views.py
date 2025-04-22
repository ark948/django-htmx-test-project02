from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_htmx.http import HttpResponseClientRedirect
import warnings

from .models import CustomUser

# Create your views here.



def index(request):
    return HttpResponse('accounts index')



@require_http_methods(['POST'])
def signup_user(request: HttpRequest):
    pass



@require_http_methods(['POST'])
def login_user_htmx(request: HttpRequest):
    warnings.warn("Authentication using HTMX is unsafe.")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        print("\n\nWRONG CREDENTIALS\n\n")
    context = { 'user': user }
    resposne = render(request, 'accounts/partials/user-status-partials/logged-in.html#user-data', context=context)
    resposne['HX-Trigger'] = 'success'
    return resposne



@require_http_methods(['POST'])
def login_user(request: HttpRequest) -> HttpResponse:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('home:index'))



def logout_user(request: HttpRequest) -> None:
    if request.method == "POST" and request.htmx:
        print("\n --> Request Reqgular POST + HTMX\n")
        logout(request)
    elif request.method == "POST":
        print("\nOnly POST\n")
        logout(request)
    else:
        print("\nError\n")
    return redirect(reverse('home:index'))