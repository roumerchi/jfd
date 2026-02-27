from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.models import Contacts
from contacts.serializers import ContactsSerializer
from core.utils import custom_exception
from services.contacts.services import delete_object, get_objects_list, check_request, update_object, get_object_by_id


class ContactsApiView(APIView):
    def get(self, request):
        """get list of contacts"""
        amount = request.query_params.get('amount')
        objects = get_objects_list(model=Contacts, amount=amount)
        return Response(ContactsSerializer(objects, many=True).data)

    @custom_exception
    def post(self, request):
        """add new contact to the list"""
        data = check_request(request.data.get('data'))
        serializer = ContactsSerializer(data=data, context={'method': 'POST'})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ContactApiView(APIView):
    def get(self, request, contact_id):
        """get specific contact"""
        obj = get_object_by_id(model=Contacts, pk=contact_id)
        return Response(ContactsSerializer(obj, many=True).data)

    @custom_exception
    def patch(self, request, contact_id):
        """update specific contact"""
        data = check_request(request.data.get('data'))

        serializer = ContactsSerializer(data=data, context={'method': 'PATCH'})
        serializer.is_valid(raise_exception=True)

        updated_object = update_object(model=Contacts, pk=contact_id, **serializer.validated_data)
        return Response(ContactsSerializer(updated_object, many=False))

    @custom_exception
    def delete(self, request, contact_id):
        """remove specific contact"""
        delete_object(model=Contacts, pk=contact_id)
        return Response(f'Contact with id {contact_id} was deleted succesfully', status=status.HTTP_204_NO_CONTENT)
