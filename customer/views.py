from django.shortcuts import render, redirect
from cashier.models import *
from .filters import ItemFilter
from .forms import AddressForm
from django.contrib import messages

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

def checkout(request):
    context = {}

    if request.user.is_authenticated:
        customer = request.user.customer
        form = AddressForm(initial={'customer': customer})
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.ordereditem_set.all()
        addresses = customer.address_set.all()
        payment_methods = PaymentMethod.objects.all()
        context = {
            'order':order, 
            'order_items':order_items, 
            'addresses':addresses, 
            'payment_methods': payment_methods,
            'form':form,
        }      
    
    if request.method == "POST":
        if 'barangay' in request.POST:
            customer = request.user.customer
            form = AddressForm(request.POST)
            if form.is_valid():
                home_phone = form.cleaned_data.get("home_phone")
                zip_code = form.cleaned_data.get("zip_code")
                if not home_phone.isnumeric():
                    messages.error(request, "Error - Phone Number is not valid")
                elif not zip_code.isnumeric():
                    messages.error(request, "Error - Zip Code is not valid")
                else:
                    form.save()


        elif 'payment' in request.POST:
            order = Order.objects.get(customer=request.user.customer, complete=False)

            order.complete = True
            order.address = Address.objects.get(id = request.POST.get('address'))
            order.payment_method = PaymentMethod.objects.get(id = request.POST.get('payment'))
            order.receive_date = request.POST.get('date')

            post_time_hour = str(request.POST.get('time'))[:2]
            post_time_minute = str(request.POST.get('time'))[-2:]
            order.recieve_time = f"{post_time_hour}:{post_time_minute}"

            order.save()
            return redirect('shop')

    return render(request, 'customer/checkout.html', context)