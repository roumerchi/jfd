from core.utils import CustomException

def to_int(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return None
    else:
        return value

def check_request(data, multiple=False):
    if not data:
        raise CustomException('"data" is required')
    if multiple:
        return data
    data = data[0]
    return data

def get_object_by_id(model, pk):
    obj = model.objects.filter(pk=pk)
    return obj

def advanced_get(model, **kwargs):
    try:
        queryset = model.objects.get(**kwargs)
    except model.DoesNotExist as e:
        raise CustomException(f'{e}')
    return queryset

def update_object(model, pk, **fields):
    obj = advanced_get(model, pk=pk)
    for field, value in fields.items():
        setattr(obj, field, value)
    obj.save()
    return obj

def delete_object(model, pk):
    obj = advanced_get(model, pk=pk)
    return obj.delete()

def get_objects_list(model, amount):
    data = model.objects.all()[:to_int(amount)].order_by('-id') # to_int usage is bad?
    return data
