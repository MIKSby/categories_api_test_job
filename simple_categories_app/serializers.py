from typing import Dict, Any, List

from rest_framework import serializers

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
