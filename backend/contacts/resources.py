from import_export import resources

from .models import Contact



class ContactModelResource(resources.ModelResource):
    class Meta:
        model = Contact