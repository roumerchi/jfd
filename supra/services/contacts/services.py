from core.utils import CustomException

def get_object_by_id(model, pk):
    obj = model.objects.filter(id=pk)
    return obj

def advanced_get(model, **kwargs):
    try:
        queryset = model.objects.get(**kwargs)
    except model.DoesNotExist as e:
        raise CustomException(f'{e}')
    return queryset

def update_object(model, pk, **fields):
    obj = advanced_get(model, id=pk)
    for field, value in fields.items():
        setattr(obj, field, value)
    obj.save()
    return obj

def delete_object(model, pk):
    obj = advanced_get(model, id=pk)
    return obj.delete()

def get_objects_list(model):
    return model.objects.all().order_by('-id')
