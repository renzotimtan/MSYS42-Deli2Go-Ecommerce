from django.shortcuts import render, redirect
from .forms import *
from .models import Item
from django.db.models import Q
from django.contrib import messages

# filters
from customer.filters import ItemFilter

def dashboard(request):
    return render(request, 'cashier/dashboard.html')

def edit_inventory(request):
    # Filter Items
    items = Item.objects.all()

    item_filter = ItemFilter(request.GET, queryset=items)
    items = item_filter.qs

    context = {
        'items':items,
        'item_filter':item_filter
    }
    return render(request, 'cashier/edit_inventory.html', context)

def add_items(request):
    form = ItemForm()
    context = {
        'form': form,
    }

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
            

    return render(request, 'cashier/add_items.html', context)