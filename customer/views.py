from django.shortcuts import render
from cashier.models import *
from .filters import ItemFilter

# Create your views here.
def shop(request):
    items = Item.objects.all()

    item_filter = ItemFilter(request.GET, queryset=items)
    items = item_filter.qs

    context = {
        'items':items,
        'item_filter':item_filter
    }
    return render(request, 'customer/shop.html', context)

def view_item(request, pk):

    item = Item.objects.get(id=pk)
    context = {
        'item':item
    }
    return render(request, 'customer/item.html', context)