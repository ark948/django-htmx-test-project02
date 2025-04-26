from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from http import HTTPStatus
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from neapolitan.views import CRUDView


from .models import Contact

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "contacts/index.html", status=HTTPStatus.OK) # 200



@login_required
def contacts_list(request: HttpRequest) -> HttpResponse:
    context = {}
    user_contacts = Contact.objects.filter(user=request.user).order_by('-created_at')
    context["contacts"] = user_contacts
    return render(request, "contacts/contacts_list.html", context)




class ContactsListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Contact
    template_name = "contacts/contacts_list.html"
    context_object_name = 'contacts'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(ContactsListView, self).get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created_at')
    


class ProtectedTestView(mixins.UserPassesTestMixin, generic.TemplateView):
    template_name = "secret.html"
    
    def test_func(self) -> bool | None:
        return self.request.user.is_active

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class ContactView(CRUDView):
    model = Contact
    fields = ["first_name", "last_name", "email", "phone_number", "address", "created_at"]