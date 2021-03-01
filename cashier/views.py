from django.shortcuts import render
from .forms import *

def add_order(request):
    form = ItemForm()
    context = {
        'form': form
    }

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    return render(request, 'cashier/add_items.html', context)