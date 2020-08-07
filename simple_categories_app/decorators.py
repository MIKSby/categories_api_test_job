import functools
from typing import cast, TypeVar, Callable, Any

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from simple_categories_app.models import Category

TFunc = TypeVar('TFunc', bound=Callable)  # type: ignore


def validate_category(func: TFunc) -> TFunc:
    @functools.wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        view = args[0]
        category_id = view.kwargs.get('category_id', None)

        try:
            category_obj = Category.objects.get(id=category_id)
        except (Category.DoesNotExist, ValidationError):
            return Response({'id': ['The requested resource was not found on this server.', ]}, status=status.HTTP_404_NOT_FOUND)

        kwargs['category_obj'] = category_obj
        return func(*args, **kwargs)

    return cast(TFunc, decorated)
