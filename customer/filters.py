import django_filters
from cashier.models import *
from django_filters import NumberFilter, CharFilter

class ItemFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    brand = CharFilter(field_name='brand', lookup_expr='icontains')
    min_price = NumberFilter(field_name='price', lookup_expr="gte")
    max_price = NumberFilter(field_name='price', lookup_expr="lte")

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['image', 'stock']
