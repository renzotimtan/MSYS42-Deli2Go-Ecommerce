from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib import messages

# Paginator
from django.core.paginator import Paginator

# filters
from customer.filters import ItemFilter
from .filters import OrderFilter

# json
import json
from django.http import JsonResponse

def dashboard(request):
    return render(request, 'cashier/dashboard.html')


# EDIT INVENTORY
def edit_inventory(request):
    # Filter Items
    items = Item.objects.all().order_by('-brand')
    item_filter = ItemFilter(request.GET, queryset=items)
    items = item_filter.qs

    # Pagination
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    items_list = paginator.get_page(page_number)

    # URL copy
    get_copy = request.GET.copy()
    if get_copy.get('page'):
        get_copy.pop('page')

    context = {
        'item_filter':item_filter,
        'items_list': items_list,
        'get_copy': get_copy
    }
    return render(request, 'cashier/edit_inventory.html', context)

def add_items(request):
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.cleaned_data.get("brand")
            name = form.cleaned_data.get("name")

            # check if duplicate
            duplicates = Item.objects.filter(Q(name=name) & Q(brand=brand))
            if not len(duplicates):
                form.save()
                messages.success(request, f"{brand} {name} has been successfully added.")
                return redirect('edit-inventory')
            else:
                messages.error(request, "Item already exists")
                form = ItemForm(request.POST, request.FILES)
                return render(request, 'cashier/add_items.html', {'form': form})
            
    context = {
        'form': form,
    }

    return render(request, 'cashier/add_items.html', context)

def edit_items(request, pk):
    item = Item.objects.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            brand = form.cleaned_data.get("brand")
            name = form.cleaned_data.get("name")

            # check if duplicate
            duplicates = Item.objects.filter(Q(name=name) & Q(brand=brand))
            if (name == item.name and brand == item.brand):
                form.save()
                messages.success(request, f"{brand} {name} has been successfully edited.")
                return redirect('edit-inventory')
            elif not len(duplicates):
                form.save()
                messages.success(request, f"{brand} {name} has been successfully added.")
                return redirect('edit-inventory')
            else:
                messages.error(request, "Item already exists")
                form = ItemForm(request.POST, request.FILES)
                return render(request, 'cashier/edit_items.html', {'form': form})
    
    context = {
        'form': form,
        'item':item,
    }

    return render(request, 'cashier/edit_items.html', context)

def delete_items(request):

    data = json.loads(request.body)
    item = Item.objects.get(id=data['item'])
    item.delete()
    messages.success(request, f"{item.name} has been deleted")
    
    return JsonResponse("Item Deleted", safe=False)

# VIEW CUSTOMER ORDERS
def customer_orders(request):
    # Filter Orders
    orders = Order.objects.filter(complete=True).order_by("receive_date")
    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders_list = paginator.get_page(page_number)

     # URL copy
    get_copy = request.GET.copy()
    if get_copy.get('page'):
        get_copy.pop('page')

    # Get ordered-items
    ordered_items = OrderedItem.objects.all() 

    # Get Categories
    status_list = OrderStatus.objects.all()

    context = {
        'order_filter': order_filter,
        'orders_list': orders_list,
        'get_copy': get_copy,
        'ordered_items': ordered_items,
        'status_list':status_list
    }
    return render(request, 'cashier/customer_orders.html', context)
    
def change_status(request):
    data = json.loads(request.body)
    status = data['status']
    orderId = data['order']
    
    order = Order.objects.get(id=orderId)
    status = OrderStatus.objects.get(status=status)

    order.order_status = status
    order.save()

    return JsonResponse("Status Changes", safe=False)
