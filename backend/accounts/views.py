from django.shortcuts import render, redirect
from django.urls import reverse, resolve, Resolver404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_htmx.http import HttpResponseClientRedirect
from django.contrib import messages
from django_htmx.http import retarget
import warnings
import logging
from django.utils.encoding import iri_to_uri
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme



from .models import CustomUser
from .forms import RegistrationForm

# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse('accounts index')



def safe_redirect(request, next_url, fallback_url = settings.LOGIN_REDIRECT_URL):
    print("\n", next_url, "\n")
    if next_url:
        next_url = iri_to_uri(next_url)
        if url_has_allowed_host_and_scheme(
            url=next_url, 
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()
        ):
            try:
                resolve(next_url)
                return HttpResponseRedirect(next_url)
            except Resolver404:
                logger.exception(f"Failed to resolve the next_url: {next_url}")
                return HttpResponseRedirect(fallback_url)
        else:
            return HttpResponseRedirect(fallback_url)
    else:
        return redirect(reverse("home:index"))



@require_http_methods(['POST'])
def signup_user(request: HttpRequest):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                print("\nUser successfully creatd.\n")
                return redirect(reverse("home:index"))
            except Exception as error:
                print("\nERROR:", error, "\n")
                return redirect(reverse("home:index"))
        else: # in case of form errors
            # context = { 'form': form }
            # response = render(request, "accounts/signup.html", context)
            # return retarget(response, "")
            print("\n", form.errors)
            return redirect(reverse("home:index"))
    context = { 'form': RegistrationForm() }
    return render(request, "accounts/signup.html")



# not used
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
    response = render(request, 'accounts/partials/user-status-partials/logged-in.html#user-data', context=context)
    response['HX-Trigger'] = 'success'
    return response




@require_http_methods(['GET', 'POST'])
def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            username = request.POST["username"] # username = request.POST.get("username", None) provide default
            password = request.POST["password"]
        except Exception as error:
            print("\nUsername or Password was not accessed.\n")
            messages.warning(request, "Unfortunately, We were unable to process your request, please try again later. (no USERNAME or PASSWORD)")
            return redirect(reverse("home:index"))
        user = authenticate(username=username, password=password)
        if user is not None:
            nxt = request.GET.get("next", None)
            login(request, user)
            # return redirect(reverse('home:index'))
            return safe_redirect(request, next_url=nxt)
        else:
            messages.warning(request, "Unfortunately, We were unable to process your request, please try again later.")
            return redirect(reverse("home:index"))
    return render(request, "accounts/login.html")



def logout_user(request: HttpRequest) -> None:
    if request.method == "POST" and request.htmx:
        # print("\n --> Request Reqgular POST + HTMX\n")
        logout(request)
    elif request.method == "POST":
        # print("\nOnly POST\n")
        logout(request)
    else:
        print("\nError\n")
    return redirect(reverse('home:index'))