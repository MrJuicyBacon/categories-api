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

    def _create_children_objects_from_dict(self, validated_data, parent=None):
        children = []
        if 'children' in validated_data:
            children = validated_data['children']
            del validated_data['children']
        category = Category(**validated_data, parent=parent)
        category.save()
        for child in children:
            self._create_children_objects_from_dict(child, category)
        return category

    def create(self, validated_data):
        with transaction.atomic():
            main_category = self._create_children_objects_from_dict(validated_data)
        return main_category

    class Meta:
        model = Category
        fields = ['name', 'children']

    def to_representation(self, instance):
        serializer = CategoryRetrieveSerializer(instance)
        return serializer.data
