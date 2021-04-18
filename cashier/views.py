from django.shortcuts import render, redirect
from .forms import *
from .models import Item
from django.db.models import Q
from django.contrib import messages

# Paginator
from django.core.paginator import Paginator

# filters
from customer.filters import ItemFilter

# json
import json
from django.http import JsonResponse

def dashboard(request):
    return render(request, 'cashier/dashboard.html')

def edit_inventory(request):
    # Filter Items
    items = Item.objects.all().order_by('-brand')

    item_filter = ItemFilter(request.GET, queryset=items)
    items = item_filter.qs

    # Pagination
    paginator = Paginator(items, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # URL copy
    get_copy = request.GET.copy()
    if get_copy.get('page'):
        get_copy.pop('page')

    context = {
        'items':items,
        'item_filter':item_filter,
        'items_list': page_obj,
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
