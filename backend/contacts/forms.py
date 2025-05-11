from django import forms
from django.core.exceptions import ValidationError

from .models import Contact


class NewConctactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')

    # dummy validation, replace with real one
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.startswith('x'):
            raise ValidationError('No names start with x!')
        return first_name


class ContactItemEditForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')

    # dummy validation, replace with real one
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.startswith('X'):
            raise ValidationError('No names start with X!')
        return first_name



class CsvFileImportForm(forms.Form):
    file = forms.FileField(label="CSV file:")