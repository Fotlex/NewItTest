from rest_framework import generics

from .models import Category, Subcategory
from .serializers import CategorySerializer, SubcategorySerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().order_by("name")
        type_id = self.request.query_params.get("type_id")
        if type_id:
            try:
                queryset = queryset.filter(type_id=int(type_id))
            except (ValueError, TypeError):
                return Category.objects.none()
        else:
            return Category.objects.none()
        return queryset


class SubcategoryListView(generics.ListAPIView):
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        queryset = Subcategory.objects.all().order_by("name")
        category_id = self.request.query_params.get("category_id")
        if category_id:
            try:
                queryset = queryset.filter(category_id=int(category_id))
            except (ValueError, TypeError):
                return Subcategory.objects.none()
        else:
            return Subcategory.objects.none()
        return queryset
