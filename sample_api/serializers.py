from .models import Category
from rest_framework import serializers
from django.db import transaction


# Serializer for internal items
class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# Main serializer for retrieving Category objects
class CategoryRetrieveSerializer(serializers.ModelSerializer):
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    siblings = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parents', 'children', 'siblings']

    @staticmethod
    def get_parents(obj):
        return SimpleCategorySerializer(obj.parents(), many=True).data

    @staticmethod
    def get_children(obj):
        return SimpleCategorySerializer(obj.children, many=True).data

    @staticmethod
    def get_siblings(obj):
        return SimpleCategorySerializer(obj.siblings(), many=True).data


# Accessory field for CategoryCreateSerializer
class ChildrenField(serializers.ListField):
    def to_representation(self, value):
        return

    def to_internal_value(self, data):
        serializer = CategoryCreateSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


# Main serializer for creating Category objects
class CategoryCreateSerializer(serializers.ModelSerializer):
    children = ChildrenField(required=False)

    def create_children_objects_from_dict(self, parent_object, children):
        for child in children:
            child_object = Category(name=child['name'], parent=parent_object)
            child_object.save()
            if 'children' in child:
                self.create_children_objects_from_dict(child_object, child['children'])
        return True

    def create(self, validated_data):
        with transaction.atomic():
            main_category = Category(name=validated_data['name'])
            main_category.save()
            if 'children' in validated_data:
                self.create_children_objects_from_dict(main_category, validated_data['children'])
        return main_category

    class Meta:
        model = Category
        fields = ['name', 'children']

    def to_representation(self, instance):
        serializer = CategoryRetrieveSerializer(instance)
        return serializer.data
