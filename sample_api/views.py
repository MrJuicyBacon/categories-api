from .models import Category
from rest_framework import generics
from .serializers import CategoryRetrieveSerializer


#  View for retrieving a single category
class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategoryRetrieveSerializer
    queryset = Category.objects.all()
