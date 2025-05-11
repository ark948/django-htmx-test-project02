from typing import Any
from http import HTTPStatus
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, FileResponse, HttpResponseBadRequest
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from neapolitan.views import CRUDView
from tablib import Dataset


from .models import Contact
from .resources import ContactModelResource
from .filters import ContactFilter
from . import forms

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "contacts/index.html", status=HTTPStatus.OK)



@login_required
def contacts_list(request: HttpRequest) -> HttpResponse:
    context = {}
    user_contacts_filter = ContactFilter(
        request.GET,
        queryset=request.user.contacts.all()
    )
    context["filter"] = user_contacts_filter
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
        else:
            context['form'] = form # will contain errors
            context['item_id'] = item.pk
            response = render(request, "contacts/partials/item-data/item-edit.html", context, status=HTTPStatus.UNPROCESSABLE_ENTITY)
            # if form contains errors, we do not want to replace the current target,
            # we must just replace the modal form itself, with the new form containing errors
            # so we use retarget 
            response['HX-Retarget'] = "#item_data"
            # response['HX-Reswap'] = 'outerHTML' # not necessary in our case
            # response['HX-Trigger-After-Settle'] = "fail" # to keep the modal open - not necessary in our case
            return response
    context['form'] = forms.ContactItemEditForm(initial=model_to_dict(item))
    context['item_id'] = item.pk
    response = render(request, "contacts/partials/item-data/item-edit.html", context)
    response["HX-Trigger"] = 'success'
    return response


@login_required
def contact_edit_2(request: HttpRequest, pk: int):
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
            messages.success(request, "Edit ok")
            return redirect(reverse("contacts:list"))
    form = forms.ContactItemEditForm(initial=model_to_dict(item))
    context['form'] = form
    context['item'] = item
    return render(request, "contacts/non-htmx/edit.html", context)



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



@login_required
def export_csv(request: HttpRequest) -> FileResponse:
    if request.htmx:
        # if request is done by htmx:
        # this will perform a client side redirect, to this very same url
        # but this time, it won't be htmx request, it will be a regular request
        return HttpResponse( headers={'HX-Redirect': request.get_full_path()} )
    queryset = request.user.contacts.all()
    data = ContactModelResource().export(queryset)
    response = HttpResponse(data.csv) # other available formats: json, yaml (requires tablib[yaml])
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    return response



@login_required
def import_csv(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        file = request.FILES.get('file')
        resource = ContactModelResource()
        dataset = Dataset()
        dataset.load(file.read().decode(), format='csv')
        result = resource.import_data(dataset=dataset, user=request.user, dry_run=True)

        for row in result:
            for error in row.errors:
                print("ROW error ->", error)

        if not result.has_errors():
            resource.import_data(dataset=dataset, user=request.user, dry_run=False)
            context['message'] = f"{len(dataset)} contacts were added successfully."
            return render(request, "contacts/partials/import-message.html", context=context)
        else:
            context['message'] = "Sorry, we were unable to process the file, Please check it and try again."
            return render(request, "contacts/partials/import-message.html", context=context)
    else:
        context['form'] = forms.CsvFileImportForm()
        return render(request, "contacts/partials/item-data/import-file.html", context=context)



@login_required
def search_within_contacts_emails(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        email_to_search = request.POST.get('email', '')
        if email_to_search == "":
            return redirect(redirect("contacts:list"))
        contacts = Contact.objects.filter(user=request.user).all()
        context['results'] = [i for i in contacts if email_to_search in i.email]
        response = render(request, "contacts/partials/search/search-result.html", context=context)
        return response
    


@login_required
def search_within_contacts_phone_number(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        phone_number_to_search = request.POST.get('phone_number', '')
        if phone_number_to_search == "":
            return redirect(reverse("contacts:list"))
        contacts = Contact.objects.filter(user=request.user).all()
        context['results'] = [i for i in contacts if phone_number_to_search in i.phone_number]
        response = render(request, "contacts/partials/search/search-result.html", context=context)
        return response



@login_required
def compound_search(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        p = request.POST.get('phone_number')
        e = request.POST.get('email')
        contacts = Contact.objects.filter(user=request.user).all()
        context['results'] = [i for i in contacts if p in i.phone_number and e in i.email]
        response = render(request, "contacts/partials/search/search-result.html", context=context)
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