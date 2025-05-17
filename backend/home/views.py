from django.views.generic import TemplateView
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.translation import gettext as _


# Create your views here.


class IndexPage(TemplateView):
    template_name = 'home/index.html'



def translate_test_view(request: HttpRequest) -> HttpResponse:
    # Translators: This message appears on the home page only
    output = _("Welcome to this site.")
    return HttpResponse(output)