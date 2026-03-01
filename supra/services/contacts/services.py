from django.db import transaction

from core.utils import CustomException

def advanced_get(model, **kwargs):
    try:
        queryset = model.objects.get(**kwargs)
    except model.DoesNotExist as e:
        raise CustomException(f'{e}')
    return queryset

def delete_object(model, pk, **kwargs):
    obj = advanced_get(model, id=pk, **kwargs)
    return obj.delete()

def get_objects_list(model, **kwargs):
    return model.objects.filter(**kwargs).order_by('-id')

def bulk_create(model, content: list):
    with transaction.atomic():
        model.objects.bulk_create(content)
