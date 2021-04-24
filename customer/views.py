from django.shortcuts import render, redirect

# models
from cashier.models import *

# filters
from .filters import ItemFilter

# forms
from .forms import AddressForm, RegisterForm, ImageUploadForm

# messages
from django.contrib import messages

# json
import json
from django.http import JsonResponse

# auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group

# Paginator
from django.core.paginator import Paginator

# -----------------------------------------------------------AUTHENTICATION-------------------------------------------------------------
@unauthenticated_user
def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password is incorrect")
    return render(request, 'customer/login.html')

@unauthenticated_user
def registerUser(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # get data
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            mobile_phone = form.cleaned_data.get("mobile_phone")

            # Check if email is taken
            if User.objects.filter(email=email).count() != 0:
                messages.error(request, "Email address has been taken")
            else:
                user = form.save()
                messages.success(request, "Account was created for " + username + "! Please login to continue.")

                # Create customer
                Customer.objects.create(
                    user=user,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    mobile_phone=mobile_phone
                )

                # Add to group
                group = Group.objects.get(name="Customer")
                user.groups.add(group)


                return redirect('login')

    context = {'form':form}
    return render(request, 'customer/register.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('login')

# ------------------------------------------------------------------------------------------------------------------------------------------




# ----------------------------------------------------------------DASHBOARD------------------------------------------------------------------
@login_required(login_url="login")
def dashboard(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    if group == "Cashier":
        return render(request, 'cashier/dashboard.html')

    return render(request, 'customer/dashboard.html')

@login_required(login_url="login")
@allowed_users(allowed_roles=['Customer'])
def addresses(request):
    customer = request.user.customer
    addresses = customer.address_set.all()
    context = {'addresses':addresses}
    return render(request, 'customer/dashboard/addresses/addresses.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Customer'])
def add_address(request):
    # Address form
    customer = request.user.customer
    form = AddressForm(initial={'customer': customer})
    context = {'form': form}

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            # Validate if home_phone and zip_code are all numbers
            home_phone = form.cleaned_data.get("home_phone")
            zip_code = form.cleaned_data.get("zip_code")
            if not home_phone.isnumeric():
                messages.error(request, "Error - Phone Number is not valid")
                context = {'form': form}
            elif not zip_code.isnumeric():
                messages.error(request, "Error - Zip Code is not valid")
                context = {'form': form}
               # If valid, save
            else:
                form.save()
                messages.success(request, "Success - New Address has been created")
                return redirect('addresses')

    return render(request, 'customer/dashboard/addresses/add_address.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Customer'])
def edit_address(request, pk):
    # Address form
    address = Address.objects.get(pk=pk)
    form = AddressForm(instance=address)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            # Validate if home_phone and zip_code are all numbers
            home_phone = form.cleaned_data.get("home_phone")
            zip_code = form.cleaned_data.get("zip_code")
            if not home_phone.isnumeric():
                messages.error(request, "Error - Phone Number is not valid")
                context = {'form': form}
            elif not zip_code.isnumeric():
                messages.error(request, "Error - Zip Code is not valid")
                context = {'form': form}
               # If valid, save
            else:
                form.save()
                messages.success(request, "Success - Address has been updated")
                return redirect('addresses')

    context = {'form': form}
    return render(request, 'customer/dashboard/addresses/edit_address.html', context)

def delete_address(request):
    data = json.loads(request.body)
    address = Address.objects.get(id=data['address'])
    address.delete()
    messages.success(request, "Success - Address has been deleted")
    
    return JsonResponse("Address Deleted", safe=False)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Customer'])
def order_status(request):
    orders = Order.objects.filter(customer=request.user.customer, complete=True).order_by("receive_date")
    # Get ordered-items
    ordered_items = OrderedItem.objects.all() 
    context = {
            "orders":orders,
            "ordered_items":ordered_items
        }
    return render(request, 'customer/dashboard/orders/order_status.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Customer'])
def upload_proof(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            order = Order.objects.get(id=pk)
            order.proof_of_payment = form.cleaned_data['image']
            order.save()
            messages.success(request, "Proof of Payment has been successfully uploaded")
    context = {'order':order}
    return render(request, 'customer/dashboard/orders/upload_proof.html', context)

# -------------------------------------------------------------------------------------------------------------------------------------------------





# --------------------------------------------------------------------SHOP-----------------------------------------------------------------------
def shop(request):
    # Filter Items
    items = Item.objects.all()

    item_filter = ItemFilter(request.GET, queryset=items)
    items = item_filter.qs

    #Pagination
    paginator = Paginator(items, 2)
    page_number = request.GET.get('page')
    items_list = paginator.get_page(page_number)

    #URL copy
    get_copy = request.GET.copy()
    if get_copy.get('page'):
        get_copy.pop('page')

    context = {
        'items_list':items_list,
        'item_filter':item_filter,
        'get_copy':get_copy
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
                    context = {
                        'order':order, 
                        'order_items':order_items, 
                        'addresses':addresses, 
                        'payment_methods': payment_methods,
                        'form':form,
                    }    
                elif not zip_code.isnumeric():
                    messages.error(request, "Error - Zip Code is not valid")
                    context = {
                        'order':order, 
                        'order_items':order_items, 
                        'addresses':addresses, 
                        'payment_methods': payment_methods,
                        'form':form,
                    }    

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
            order.receive_time = f"{post_time_hour}:{post_time_minute}"
            status = OrderStatus.objects.get(status="Order Sent")
            print(status)
            order.order_status = status

            order.save()

            # Message success
            messages.success(request, "Order has been sent")
            return redirect('shop')
            

    return render(request, 'customer/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    itemId = data['item']

    if data.get('quantity'):
        quantity = data['quantity']
    else:
        quantity = 1

    if data.get('action'):
        action = data['action']
    else:
        action = "add"

    if request.user.is_authenticated:
        customer = request.user.customer

        # get order and item
        item = Item.objects.get(id=itemId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # check if order and item has been made
        ordered_item, created = OrderedItem.objects.get_or_create(order=order, item=item)

        if action == "add":

            # If more than stock, error
            if (int(quantity) > item.stock) or (not int(quantity)):
                messages.error(request, "Error - Exceeded stock.")
                return JsonResponse("Exceeded stock", safe=False)
            else:
                # add quantity, subtract stock
                ordered_item.quantity += int(quantity)
                item.stock -= int(quantity)
                
                ordered_item.save()
                item.save()
                messages.success(request, f"{item.name} was successfully added to cart")
            
        elif action == "remove":
            ordered_item.quantity -= int(quantity)
            item.stock += int(quantity)

            # If quantity is 0, remove ordered_item
            if ordered_item.quantity <= 0:
                ordered_item.delete()
            else:
                ordered_item.save()
            item.save()
                
            messages.success(request, f"{item.name} was successfully removed from cart")
    else:
        messages.error(request, "Please register an account before logging in")

    return JsonResponse("Cart Updated.", safe=False)
