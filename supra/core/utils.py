from rest_framework.response import Response


class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)


def custom_exception(func: callable):
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except CustomException as e:
            return Response({"error": f"{e}"}, status=400)
    return wrapper
