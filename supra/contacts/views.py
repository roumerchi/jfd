import csv
from io import TextIOWrapper

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.external import get_coordinates, get_weather
from contacts.models import Contacts, CityWeather, ContactStatus
from contacts.serializers import ContactsSerializer, ContactDetailSerializer, CityWeatherSerializer, \
    ContactsBulkSerializer, ContactsImportSerializer
from core.utils import custom_exception, CustomException
from services.contacts.services import delete_object, get_objects_list, advanced_get, bulk_create


class ContactsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ContactsApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get list of contacts",
        description=(
            "Return list of contacts.\n\n"
            "Supports ordering via `ordering` query parameter.\n"
            "Use comma-separated values.\n\n"
            "Examples:\n"
            "- ordering=last_name\n"
            "- ordering=-last_name\n"
            "- ordering=created_at\n"
            "- ordering=last_name,-created_at"
        ),
        parameters=[
            OpenApiParameter(
                name='ordering',
                description=(
                    "Ordering of results. "
                    "Use comma-separated field names. "
                    "Prefix with '-' for descending order.\n\n"
                    "Allowed fields:\n"
                    "- last_name\n"
                    "- created_at"
                ),
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={200: ContactsSerializer(many=True)}
    )
    def get(self, request):
        """get list of contacts"""
        objects = get_objects_list(model=Contacts, owner=request.user)

        ordering = request.query_params.get('ordering')
        allowed = {'last_name', '-last_name', 'created_at', '-created_at'}
        if ordering:
            fields = ordering.split(',')
            safe_fields = [f for f in fields if f in allowed]
            if safe_fields:
                objects = objects.order_by(*safe_fields)

        paginator = ContactsPagination()
        page = paginator.paginate_queryset(objects, request)
        serializer = ContactsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create new contact",
        request=ContactsSerializer,
        responses={201: ContactsSerializer},
    )
    def post(self, request):
        """add new contact to the list"""
        serializer = ContactsSerializer(data=request.data, context={'method': 'POST', 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ContactApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get specific contact",
        responses={200: ContactDetailSerializer(many=False)}
    )
    def get(self, request, contact_id):
        """get specific contact"""
        try:
            obj = advanced_get(model=Contacts, pk=contact_id, owner=request.user)
        except (Contacts.DoesNotExist, CustomException):
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactDetailSerializer(obj)
        return Response(serializer.data)

    @extend_schema(
        summary="Update specific contact",
        request=ContactDetailSerializer,
        responses={200: ContactDetailSerializer(many=False)}
    )
    def put(self, request, contact_id):
        """update specific contact"""
        try:
            contact = advanced_get(model=Contacts, pk=contact_id, owner=request.user)
        except (Contacts.DoesNotExist, CustomException):
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactDetailSerializer(
            instance=contact, data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @extend_schema(
        summary="Delete specific contact",
        responses={204: None}
    )
    @custom_exception(204)
    def delete(self, request, contact_id):
        """delete specific contact"""
        try:
            delete_object(model=Contacts, pk=contact_id, owner=request.user)
        except Contacts.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(f'Contact with id {contact_id} was deleted succesfully', status=status.HTTP_204_NO_CONTENT)


class CityWeatherAPIView(APIView):
    """GET /api/weather/?city=London"""

    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'detail': 'city parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        city = city.strip()
        weather = CityWeather.objects.filter(city__iexact=city).first()

        if weather and weather.is_fresh():
            serializer = CityWeatherSerializer(weather)
            return Response(serializer.data)
        try:
            lat, lon = get_coordinates(city)
            data = get_weather(lat, lon)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        weather, _ = CityWeather.objects.update_or_create(
            city=city,
            defaults={
                'latitude': lat,
                'longitude': lon,
                'temperature': data['temperature'],
                'wind_speed': data['windspeed'],
                'weather_code': data['weathercode'],
            }
        )

        serializer = CityWeatherSerializer(weather)
        return Response(serializer.data)


class ContactsBulkImportApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Import contacts from CSV",
        request=ContactsImportSerializer,
        responses={201: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        serializer = ContactsImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        csv_file = serializer.validated_data['file']
        decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)

        contacts, errors = [], []
        default_status = ContactStatus.objects.get(code='default')

        for index, row in enumerate(reader, start=1):
            contact_data = {
                'first_name': row.get('first_name'),
                'last_name': row.get('last_name'),
                'phone': row.get('phone'),
                'email': row.get('email'),
                'city': row.get('city'),
            }

            contact_serializer = ContactsBulkSerializer(data=contact_data)
            if contact_serializer.is_valid():
                contacts.append(Contacts(**contact_serializer.validated_data, owner=request.user, status=default_status))
            else:
                errors.append({'row': index, 'errors': contact_serializer.errors})
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        bulk_create(model=Contacts, content=contacts)

        return Response({'created': len(contacts)}, status=status.HTTP_201_CREATED)
