from typing import Dict, Any, List

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from simple_categories_app.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Category

    def to_representation(self, instance: Category) -> Dict[str, Any]:
        return_data = {
            'id': instance.id,
            'name': instance.name,
            'siblings': [],
            'parents': [],
            'children': [],
        }

        for obj in self.Meta.model.objects.filter(parent_id=instance.parent_id).exclude(id=instance.id):
            return_data['siblings'].append({x: getattr(obj, x) for x in self.Meta.fields})

        for obj in self.Meta.model.objects.filter(parent_id=instance.id):
            return_data['children'].append({x: getattr(obj, x) for x in self.Meta.fields})

        while instance.parent:
            return_data['parents'].append({x: getattr(instance.parent, x) for x in self.Meta.fields})
            instance = instance.parent
        return return_data


class CategoryCreateSerializer(serializers.Serializer):
    return_fields = ['id', 'name', 'parent_id']

    def make_return_fields(self, obj: Category) -> Dict[str, Any]:
        return {x: getattr(obj, x) for x in self.return_fields}

    def storing_json(self, array: Dict[str, Any], parent_id: int = None) -> None:
        instance = Category.objects.create(name=array['name'], parent_id=parent_id)
        self.objs.append(self.make_return_fields(instance))
        if array.get('children'):
            for children_array in array['children']:
                self.storing_json(children_array, instance.id)

    def create(self, validated_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.objs: List[Dict[str, Any]] = []
        self.storing_json(self.initial_data)
        return self.objs

    def get_names_and_check_schema(self, data: Dict[str, Any]) -> None:
        len_keys = len(data.keys())
        if not (1 <= len_keys <= 2) or 'name' not in data.keys():
            raise ValidationError('incorrect data')
        self.names.add(data['name'])

        if data.get('children') and len_keys == 2:
            for children in data['children']:
                self.get_names_and_check_schema(children)
        elif not data.get('children') and len_keys == 2:
            raise ValidationError('incorrect data')

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        self.names = set()
        self.get_names_and_check_schema(dict(self.initial_data))
        if Category.objects.filter(name__in=self.names).exists():
            raise ValidationError('category name exists')
        return attrs
