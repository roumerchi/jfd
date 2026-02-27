from rest_framework import serializers

from contacts.models import Contacts


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('status', 'first_name', 'last_name', 'phone', 'email', 'city', 'created_at')
