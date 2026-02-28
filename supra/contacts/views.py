from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.external import get_coordinates, get_weather
from contacts.models import Contacts, CityWeather
from contacts.serializers import ContactsSerializer, ContactDetailSerializer, CityWeatherSerializer
from core.utils import custom_exception
from services.contacts.services import delete_object, get_objects_list, advanced_get


class ContactsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ContactsApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get list of contacts",
        description="Return all contacts or a limited number if `amount` is provided",
        responses={200: ContactsSerializer(many=True)}
    )
    def get(self, request):
        """get list of contacts"""
        objects = get_objects_list(model=Contacts)

        paginator = ContactsPagination()
        page = paginator.paginate_queryset(objects, request)
        serializer = ContactsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Create new contact",
        request=ContactsSerializer,
        responses={201: ContactsSerializer},
    )
    @custom_exception
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
    @custom_exception
    def get(self, request, contact_id):
        """get specific contact"""
        obj = advanced_get(model=Contacts, pk=contact_id)
        serializer = ContactDetailSerializer(obj)
        return Response(serializer.data)

    @extend_schema(
        summary="Update specific contact",
        request=ContactDetailSerializer,
        responses={200: ContactDetailSerializer(many=False)}
    )
    @custom_exception
    def patch(self, request, contact_id):
        """update specific contact"""
        contact = advanced_get(model=Contacts, pk=contact_id)
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
    @custom_exception
    def delete(self, request, contact_id):
        """delete specific contact"""
        delete_object(model=Contacts, pk=contact_id)
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
