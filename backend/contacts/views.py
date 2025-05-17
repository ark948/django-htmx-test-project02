from typing import Any
from http import HTTPStatus
import csv
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
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
from django.core.exceptions import PermissionDenied


from .models import Contact
from .resources import ContactModelResource
from .filters import ContactFilter
from . import forms
from . import services

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
    context['total_contacts'] = user_contacts_filter.qs.get_total_contacts()
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
    except Contact.DoesNotExist as error:
        messages.error(request, "Such contact does not exist, or does not belong to you.")
        return redirect(reverse("contacts:list"))
    except Exception as error:
        messages.error(request, "Sorry, we encountered an unknown problem, please check your input and try again in a while.")
        return redirect(reverse("contacts:list"))
    response = render(request, "contacts/partials/item-data/item.html", context)
    response["HX-Trigger"] = 'success'
    return response


# NOT USED
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
def contact_edit_v2(request: HttpRequest, pk: int) -> HttpResponse:
    context = {}
    try:
        item = Contact.objects.get(pk=pk)
    except Exception as error:
        messages.error(request, "Sorry, we were unable to aquire this item. It may not exist.")
        return redirect(reverse("contacts:list"))
    if item.user != request.user:
        messages.error(request, "Sorry, such contact does not exist, or does not belong to you.")
        return redirect(reverse("contacts:list"))
    if request.method == "POST":
        form = forms.ContactItemEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            context['message'] = "Item edited successfully."
            response = render(request, "contacts/partials/messages/edit-success-message.html", context)
            response["HX-Trigger"] = "done"
            return response
        else:
            context['form'] = form
            context['item_id'] = item.pk
            response = render(request, "contacts/partials/forms/item-edit-form.html", context)
            # response['HX-Retarget'] = "#item_edit_form" # this has no effect
            return response
    context['form'] = forms.ContactItemEditForm(initial=model_to_dict(item))
    context['item_id'] = item.pk
    response = render(request, "contacts/partials/forms/item-edit-form.html", context)
    response['HX-Trigger'] = "success"
    return response


# NOT USED
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
    return redirect(reverse("contacts:list"))



@login_required
@require_http_methods(['DELETE'])
def delete_contact_v2(request: HttpRequest, pk: int):
    item = get_object_or_404(Contact, pk=pk)
    if item.user != request.user:
        raise PermissionDenied("You do not have permission to perform this action.")
    item.delete()
    response = HttpResponse()
    messages.info(request, "Item deleted successfully.")
    response['HX-Redirect'] = reverse("contacts:list")
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
            response = render(request, "contacts/partials/item-data/new-item.html", { "form": form }, status=HTTPStatus.UNPROCESSABLE_ENTITY)
            response['HX-Retarget'] = "#new_item_form"
            return response
    context = { 'form': forms.NewConctactForm() }
    response = render(request, "contacts/partials/item-data/new-item.html", context)
    return response



# Rewriting new contact view
@login_required
def new_contact_v2(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        form = forms.NewConctactForm(request.POST)
        if form.is_valid():
            contact: Contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            context['message'] = "New item added successfully."
            response = render(request, "contacts/partials/messages/successful-new-contact-message.html", context, status=HTTPStatus.ACCEPTED)
            response['HX-Target'] = "success"
            return response
        else:
            context['form'] = form
            # if status code is set to unprocessable entitiy (422), form errors feedback will not be displayed
            response = render(request, "contacts/partials/forms/new-contact-form.html", context=context)
            return response
    context['form'] = forms.NewConctactForm()
    return render(request, "contacts/partials/forms/new-contact-form.html", context)



@login_required
def export_csv(request: HttpRequest) -> FileResponse:
    if request.htmx:
        # if request is done by htmx:
        # this will perform a client side redirect, to this very same url
        # but this time, it won't be htmx request, it will be a regular request
        return HttpResponse( headers={'HX-Redirect': request.get_full_path()} )
    
    # other available formats: json, yaml (requires tablib[yaml])
    response = HttpResponse( services.write_csv(request.user.pk) )
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    return response



@login_required
def export_csv_v2(request: HttpRequest) -> FileResponse:
    if request.htmx:
        return HttpResponse( headers = {'HX-Redirect': request.get_full_path()} )
    contacts_filter = ContactFilter(
        request.GET,
        queryset=Contact.objects.filter(user=request.user)
    )
    data = ContactModelResource().export(contacts_filter.qs)
    response = HttpResponse(data.csv)
    response['Content-Disposition'] = "attachment; filename=contacts.csv"
    return response



@login_required
@require_http_methods(['POST'])
def export_email_search_results(request: HttpRequest) -> HttpResponse:
    data = request.POST['term']
    try:
        contacts = Contact.objects.filter(user=request.user).all()
        results = [i for i in contacts if data in i.email]
    except Exception as error:
        print("\nERROR->", error)
        messages.error(request, "Sorry, there was a problem. This action is not possible right now.")
        return redirect(reverse('contacts:list'))
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="filtered_contacts.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["first_name", "last_name", "email", "phone_number", "address", "created_at"])
    for item in results:
        writer.writerow([item.first_name, item.last_name, item.email, item.phone_number, item.address, item.created_at])
    return response
    


@login_required
def import_csv(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        file = request.FILES.get('file')
        resposne = services.read_csv(file=file, user=request.user)
        if resposne['status'] == True:
            context['message'] = f"{resposne['count']} contacts were added successfully."
        elif resposne['status'] == False:
            context['message'] = "Sorry, we were unable to process the file, Please check it and try again."
        return render(request, "contacts/partials/messages/file-action-message.html", context=context)
    return render(request, "contacts/partials/forms/csv-file-import-form.html", context={'form': forms.CsvFileImportForm()})



# NOT USED
@login_required
def search_within_contacts_emails(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        email_to_search = request.POST.get('email', '')
        if email_to_search == "":
            return redirect(reverse("contacts:list"))
        contacts = Contact.objects.filter(user=request.user).all()
        context['results'] = [i for i in contacts if email_to_search in i.email]
        context['results_count'] = len(context['results'])
        response = render(request, "contacts/partials/contacts-list-container.html", context=context)
        return response
    

@login_required
@require_http_methods(['POST'])
def search_within_contacts_emails_v2(request: HttpRequest) -> HttpResponse:
    context = {}
    email_term = request.POST.get('email')
    if not email_term: # not working
        messages.error(request, "Error in search. Invalid parameter.")
        return redirect(reverse('contacts:list'))
    contacts = Contact.objects.filter(user=request.user).all()
    results = [i for i in contacts if email_term in i.email]
    context['results'] = results
    context['results_count'] = len(results)
    context['term'] = email_term
    response = render(request, "contacts/partials/search/search-results-container.html", context=context)
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
        response = render(request, "contacts/partials/search/search-results.html", context=context)
        return response



@login_required
def compound_search(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        p = request.POST.get('phone_number')
        e = request.POST.get('email')
        contacts = Contact.objects.filter(user=request.user).all()
        context['results'] = [i for i in contacts if p in i.phone_number and e in i.email]
        response = render(request, "contacts/partials/search/search-results.html", context=context)
        return response
    


@login_required
@require_http_methods(['PUT'])
def item_inline_edit(requset: HttpRequest) -> HttpResponse:
    pass



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