from rest_framework.response import Response


class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)


def custom_exception(status=400):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CustomException as e:
                return Response({"error": str(e)}, status=status)
        return wrapper
    return decorator
