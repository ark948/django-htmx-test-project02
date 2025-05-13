from import_export import resources

from .models import Contact



class ContactModelResource(resources.ModelResource):

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.user = kwargs.get('user') # attach the user to every record (as the owner)

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

        # import_id_fields -> if all fields of a record match an existing record,
        # then do not add that record
        # sort of like a unique constraint
        # THIS DOES NOT WORK for some reason
        import_id_fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'created_at'
        )




# for imports (csv upload),
# a user must be automatically tied to all records