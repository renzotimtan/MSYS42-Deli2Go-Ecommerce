from django.shortcuts import render
from .forms import *
from .models import Item
from django.db.models import Q
from django.contrib import messages

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
            else:
                messages.error(request, "Item already exists")
                form = ItemForm(request.POST, request.FILES)
                return render(request, 'cashier/add_items.html', {'form': form})
            

    return render(request, 'cashier/add_items.html', context)