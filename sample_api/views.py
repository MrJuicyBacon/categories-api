from .models import Category
from rest_framework import generics
from .serializers import CategoryRetrieveSerializer, CategoryCreateSerializer


#  View for retrieving a single category
class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategoryRetrieveSerializer
    queryset = Category.objects.all()


# View for creating categories (including nested ones)
class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategoryCreateSerializer
