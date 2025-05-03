from django import forms

from .models import Contact


class ContactItemEditForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')