from typing import Any

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from simple_categories_app.decorators import validate_category
from simple_categories_app.models import Category
from simple_categories_app.serializers import CategorySerializer, CategoryCreateSerializer


class CategoryDetailsView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @validate_category
    def get(self, request: Request, category_obj: Category, *args: Any, **kwargs: Any) -> Response:
        serializer: CategorySerializer = self.get_serializer(category_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryView(GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: CategoryCreateSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance_list = serializer.save()
        return Response(instance_list, status=status.HTTP_201_CREATED)
