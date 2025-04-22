from django.shortcuts import render
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser

# Create your views here.



def index(request):
    return HttpResponse('accounts index')



@require_http_methods(['POST'])
def signup_user(request: HttpRequest):
    pass


@require_http_methods(['POST'])
def login_user(request: HttpRequest):
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



def logout_user(request: HttpRequest):
    if request.method == "POST":
        logout(request)