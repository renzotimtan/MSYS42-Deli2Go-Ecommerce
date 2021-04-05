from django.shortcuts import render, redirect
from cashier.models import *
from .filters import ItemFilter
from .forms import AddressForm
from django.contrib import messages
import json
from django.http import JsonResponse

# Create your views here.
def shop(request):
    # Filter Items
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

    # Display ordered
    if request.user.is_authenticated:
        customer = request.user.customer

        # Address form
        form = AddressForm(initial={'customer': customer})

        # Get current order and ordered items
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.ordereditem_set.all()

        # Get all customer addresses
        addresses = customer.address_set.all()

        # Get payment methods
        payment_methods = PaymentMethod.objects.all()
        context = {
            'order':order, 
            'order_items':order_items, 
            'addresses':addresses, 
            'payment_methods': payment_methods,
            'form':form,
        }      
    
    if request.method == "POST":

        # If address form is sent
        if 'barangay' in request.POST:
            customer = request.user.customer
            form = AddressForm(request.POST)
            if form.is_valid():

                # Validate if home_phone and zip_code are all numbers
                home_phone = form.cleaned_data.get("home_phone")
                zip_code = form.cleaned_data.get("zip_code")
                if not home_phone.isnumeric():
                    messages.error(request, "Error - Phone Number is not valid")
                elif not zip_code.isnumeric():
                    messages.error(request, "Error - Zip Code is not valid")

                # If valid, save
                else:
                    form.save()
                    messages.success(request, "Success - New Address has been created")

        # If order is submitted
        elif 'payment' in request.POST:
            order = Order.objects.get(customer=request.user.customer, complete=False)

            # Update order details and set complete to true
            order.complete = True
            order.address = Address.objects.get(id = request.POST.get('address'))
            order.payment_method = PaymentMethod.objects.get(id = request.POST.get('payment'))
            order.receive_date = request.POST.get('date')

            # Delivery Fee Logic
            if (order.payment_method.method != "Cash On Pickup"):
                if (order.address.city.lower() in ["quezon city", "san juan city"]):
                    order.delivery_fee = 100.00
                else:
                    order.delivery_fee = 150.00
            else:
                order.delivery_fee = 0.00

            post_time_hour = str(request.POST.get('time'))[:2]
            post_time_minute = str(request.POST.get('time'))[-2:]
            order.recieve_time = f"{post_time_hour}:{post_time_minute}"

            order.save()

            # Message success
            messages.success(request, "Success - Order has been sent")
            return redirect('shop')
            

    return render(request, 'customer/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    itemId = data['item']
    quantity = data['quantity']

    if request.user.is_authenticated:
        customer = request.user.customer

        # get order and item
        item = Item.objects.get(id=itemId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # check if order and item has been made
        ordered_item, created = OrderedItem.objects.get_or_create(order=order, item=item)

        print(ordered_item)

        # add quantity, subtract stock


        if (int(quantity) > item.stock) or (not int(quantity)):
            messages.error(request, "Error - Please enter valid quantity.")
            return JsonResponse("Exceeded stock", safe=False)

        ordered_item.quantity += int(quantity)
        item.stock -= int(quantity)

        #save
        ordered_item.save()
        item.save()
        messages.success(request, "Success - Added to Cart")

    return JsonResponse("Item was added", safe=False)
