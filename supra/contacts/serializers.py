from rest_framework import serializers

from contacts.models import Contacts, ContactStatus, CityWeather


class ContactStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactStatus
        fields = ('code', 'title')
        read_only_fields = ('code', 'title')


class ContactsSerializer(serializers.ModelSerializer):
    status = ContactStatusSerializer(read_only=True)
    status_code = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Set status by code ('default' or 'blocked')"
    )

    class Meta:
        model = Contacts
        fields = (
            'status', 'status_code', 'first_name', 'last_name', 'phone', 'email', 'city', 'created_at',
        )
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        owner = self.context['request'].user
        validated_data['owner'] = owner

        status_code = validated_data.pop('status_code', 'default')
        try:
            status_obj = ContactStatus.objects.get(code=status_code)
        except ContactStatus.DoesNotExist:
            raise serializers.ValidationError({'status_code': f"Unknown status: {status_code}"})
        validated_data['status'] = status_obj

        return super().create(validated_data)

    def update(self, instance, validated_data):
        status_code = validated_data.pop('status_code', None)
        if status_code:
            try:
                status_obj = ContactStatus.objects.get(code=status_code)
            except ContactStatus.DoesNotExist:
                raise serializers.ValidationError({'status_code': f"Unknown status: {status_code}"})
            validated_data['status'] = status_obj

        return super().update(instance, validated_data)


class ContactDetailSerializer(serializers.ModelSerializer):
    status = ContactStatusSerializer(read_only=True)
    status_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Contacts
        fields = (
            'id', 'status', 'status_code', 'first_name', 'last_name', 'phone', 'email', 'city', 'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def update(self, instance, validated_data):
        status_code = validated_data.pop('status_code', None)

        if status_code:
            try:
                instance.status = ContactStatus.objects.get(code=status_code)
            except ContactStatus.DoesNotExist:
                raise serializers.ValidationError(
                    {'status_code': f'Unknown status: {status_code}'}
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CityWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityWeather
        fields = ('city', 'temperature', 'wind_speed', 'weather_code', 'updated_at',)


class ContactsImportSerializer(serializers.Serializer):
    file = serializers.FileField()


class ContactsBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('first_name', 'last_name', 'phone', 'email', 'city',)
