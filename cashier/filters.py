import django_filters
from .models import Order, Item
from django_filters import CharFilter

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_status', 'payment_method', 'receive_date']

class ItemFilterQuantity(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    brand = CharFilter(field_name='brand', lookup_expr='icontains')

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['image', 'stock', 'price', 'description']

