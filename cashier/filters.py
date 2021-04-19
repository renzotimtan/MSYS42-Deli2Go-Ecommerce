import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_status', 'payment_method', 'receive_date']

#