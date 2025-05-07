from typing import Any
from http import HTTPStatus
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from neapolitan.views import CRUDView


from .models import Contact
from . import forms

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "contacts/index.html", status=HTTPStatus.OK)



@login_required
def contacts_list(request: HttpRequest) -> HttpResponse:
    context = {}
    user_contacts = request.user.contacts.all()
    context["contacts"] = user_contacts
    context["new_contact_form"] = forms.NewConctactForm()
    if request.htmx:
        response = render(request, "contacts/partials/contacts-list-container.html", context)
        response['HX-Trigger'] = "clean"
        return response
    else:
        return render(request, "contacts/contacts-list.html", context)



@login_required
def contact_item(request: HttpRequest, pk: int) -> HttpResponse:
    context = {}
    try:
        contact_item = Contact.objects.get(pk=pk)
        if contact_item.user == request.user:
            context['item'] = contact_item
        else:
            raise Contact.DoesNotExist
    except Exception as error:
        print("ERROR -> ", error)
        messages.error("Such contact does not exist, or does not belong to you.")
        return redirect(reverse("contacts:list"))
    response = render(request, "contacts/partials/item-data/item.html", context)
    response["HX-Trigger"] = 'success'
    return response



# REWRITE with PUT or Patch
@login_required
def contact_edit(request: HttpRequest, pk: int) -> HttpResponse:
    context = {}
    try:
        item = Contact.objects.get(pk=pk)
        if item.user != request.user:
            raise Contact.DoesNotExist("Such primary key does not exist, or does not belong to you.")
    except Exception as error:
        print("ERROR -> ", error)
        messages.error(request, "Sorry, such contact does not exist, or does not belong to you.")
        return redirect(reverse("contacts:list"))
    if request.method == "POST":
        form = forms.ContactItemEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            context["message"] = "Item edited successfully."
            response = render(request, "contacts/partials/edit-success.html", context)
            response["HX-Trigger"] = "done"
            return response
    context['form'] = forms.ContactItemEditForm(initial=model_to_dict(item))
    context['item_id'] = item.pk
    response = render(request, "contacts/partials/item-data/item-edit.html", context)
    response["HX-Trigger"] = 'success'
    return response



@login_required
@require_http_methods(["DELETE"])
def delete_contact(request: HttpRequest, pk: int) -> HttpResponse:
    context = {}
    try:
        item_to_delete = Contact.objects.get(pk=pk)
        if item_to_delete.user != request.user:
            raise Contact.DoesNotExist("Such contact does not exist, or does not belong to you.")
    except Exception as error:
        print("ERROR -> ", error)
        messages.error(request, "Sorry, such contact does not exist, or does not belong to you.")
        return redirect(reverse("contacts:list"))
    item_to_delete.delete()
    user_contacts = Contact.objects.filter(user=request.user)
    context["contacts"] = user_contacts
    response = render(request, "contacts/partials/contacts-list-container.html", context)
    return response



@login_required
def new_contact(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.NewConctactForm(request.POST)
        if form.is_valid():
            new_contact_item = form.save(commit=False)
            new_contact_item.user = request.user
            new_contact_item.save()
            response = render(request, "contacts/partials/new-item-success.html", { 'message': "Item successfully added." })
            response['HX-Trigger'] = "done"
            return response
    else:
        context = { 'form': forms.NewConctactForm() }
        response = render(request, "contacts/partials/item-data/new-item.html", context)
        return response



class ContactDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = Contact
    
    def get_context_data(self, *args, **kwargs: Any) -> dict[str, Any]: # if need to edit fields
        context = super(ContactDetailView, self).get_context_data(*args, **kwargs)
        # add extra field 
        # context["count"] = "MISC"
        return context



class ContactsListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Contact
    template_name = "contacts/contacts-list.html"
    context_object_name = 'contacts'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.htmx:
            self.template_name = "contacts/partials/contacts-list-container.html"
            response = super(ContactsListView, self).dispatch(*args, **kwargs)
            response['HX-Trigger'] = 'clean'
            return response
        else:
            response = super(ContactsListView, self).dispatch(*args, **kwargs)
            return response

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
    

# Django Neapolitan
class ContactView(mixins.LoginRequiredMixin, CRUDView):
    model = Contact
    fields = ["first_name", "last_name", "email", "phone_number", "address", "created_at"]