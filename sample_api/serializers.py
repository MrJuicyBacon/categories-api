from .models import Category
from rest_framework import serializers


# Serializer for internal items
class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# Main serializer for Category objects
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
