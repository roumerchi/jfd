from django.forms import ModelForm, ChoiceField, EmailInput, TextInput
from phonenumber_field.formfields import PhoneNumberField

from contacts.models import ContactStatus, Contacts


class ContactForm(ModelForm):
    status_code = ChoiceField(
        choices=[(status.code, status.title) for status in ContactStatus.objects.all()],
        required=False,
        initial='default'
    )
    phone = PhoneNumberField(
        region='PL',
        widget=TextInput(attrs={'placeholder': '+48 000 000 000'})
    )

    class Meta:
        model = Contacts
        fields = ['first_name', 'last_name', 'phone', 'email', 'city']
        widgets = {
            'email': EmailInput(attrs={
                'type': 'email',
                'required': True,
                'placeholder': 'john@example.com',
            }),
        }
