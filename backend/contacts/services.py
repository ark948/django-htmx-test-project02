from django.db.models import QuerySet
from django.core.files import File
from tablib import Dataset

from accounts.models import CustomUser
from .models import Contact
from .resources import ContactModelResource


# not much point in using this
def create_contact(
            first_name: str,
            last_name: str,
            email: str,
            phone_number: str,
            address: str,
            owner: CustomUser
        ) -> Contact:
    contact = Contact( first_name = first_name, last_name = last_name, emai = email, phone_number = phone_number, address = address)
    contact.user = owner
    contact.save()
    return contact



def read_csv(file: File, user: CustomUser) -> dict:
    try:
        response = {}
        resource = ContactModelResource()
        dataset = Dataset()
        dataset.load(file.read().decode(), format='csv')
        result = resource.import_data(dataset=dataset, user=user, dry_run=True)
    except Exception as error:
        print("ERROR in processing file (01).")
        response['status'] = False
        return response

    try:
        for row in result:
            for error in row.errors:
                print("ROW error ->", error)
    except Exception as error:
        print("ERROR in reading errors.")
        response['status'] = False
        return response

    try:
        if not result.has_errors():
            resource.import_data(dataset=dataset, user=user, dry_run=False)
            response['status'] = True
            response['count'] = len(dataset)
        else:
            response['status'] = False
    except Exception as error:
        print("ERROR in processing file (02).")
        response['status']
        return response
        
    return response



def write_csv(user_id: int) -> Dataset:
    try:
        queryset: QuerySet = Contact.objects.filter(user__pk=user_id)
    except Exception as error:
        print("ERROR -> ", error)
        result = None
    
    try:
        data: Dataset = ContactModelResource().export(queryset)
        result = data.csv
    except Exception as error:
        print("ERROR -> ", error)
        result = None
    
    return result


def write_csv_include_filters():
    pass