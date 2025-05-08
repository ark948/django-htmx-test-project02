from import_export import resources

from .models import Contact



class ContactModelResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'created_at'
        )




# for imports (csv upload),
# a user must be automatically tied to all records