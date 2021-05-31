from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from customer.decorators import unauthenticated_user, allowed_users

# Paginator
from django.core.paginator import Paginator

# filters
from customer.filters import ItemFilter
from .filters import OrderFilter, ItemFilterQuantity, OrderFilterProof

# json
import json
from django.http import JsonResponse

# excel
import xlwt
import tablib
from django.http import HttpResponse



# EDIT INVENTORY
@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
def edit_inventory(request):
    # Filter Items
    items = Item.objects.all().order_by('brand')
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

@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
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

@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
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

@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
def adjust_quantity(request):
    # Filter Items
    items = Item.objects.all().order_by('brand')
    item_filter = ItemFilterQuantity(request.GET, queryset=items)
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
    
    return render(request, "cashier/adjust_quantity.html", context)

def delete_items(request):
    data = json.loads(request.body)
    item = Item.objects.get(id=data['item'])
    item.delete()
    messages.success(request, f"{item.name} has been deleted")
    
    return JsonResponse("Item Deleted", safe=False)

# VIEW CUSTOMER ORDERS
@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
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
    
# PROOF OF PAYMENT
@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
def view_proof(request):
    method = PaymentMethod.objects.get(method="GCash Delivery")
    status = OrderStatus.objects.get(status="Payment Sent")
    orders = Order.objects.filter(payment_method=method, order_status=status).order_by('receive_date')
    
    # Filter Orders
    order_filter = OrderFilterProof(request.GET, queryset=orders)
    orders = order_filter.qs

    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders_list = paginator.get_page(page_number)

    # URL copy
    get_copy = request.GET.copy()
    if get_copy.get('page'):
        get_copy.pop('page')

    context = {
        'orders_list':orders_list, 
        'order_filter':order_filter, 
        'get_copy': get_copy
    }
    return render(request, 'cashier/view_proof.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
def view_proof_picture(request, pk):
    order = Order.objects.get(id=pk)
    context = {'order': order}
    return render(request, 'cashier/view_proof_picture.html', context)


def handle_proof(request, pk, action):
    order = Order.objects.get(id=pk)
    if action == "accept":
        status = OrderStatus.objects.get(status="Payment Confirmed")
        order.order_status = status
        order.save()
        messages.success(request, "Payment has been accepted")
        return redirect('view-proof')
    elif action == "decline":
        status = OrderStatus.objects.get(status="Order Confirmed")
        order.order_status = status
        order.proof_of_payment = None
        order.save()
        messages.success(request, "Payment has been declined. Please text the customer on the concern.")
        return redirect("view-proof")

# ADD DRIVER
@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
def add_driver(request):
    cash_on_pickup = PaymentMethod.objects.get(method="Cash On Pickup")
    orders = Order.objects.filter(complete=True).exclude(payment_method=cash_on_pickup).order_by("receive_date")
    drivers = Driver.objects.all()
    context = {
        'orders_list': orders,
        'drivers': drivers
    }
    return render(request, 'cashier/add_driver.html', context)

# EXPORT DATA
@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
def export_data(request):
    orders = Order.objects.all()
    months = []

    for i in orders:
        year = i.order_date.strftime("%Y")
        month = i.order_date.strftime("%m")
        full = f"{month}-{year}"

        if full not in months:
            months.append(full)
    
    print(months)
    context = {'months':months}
    return render(request, "cashier/export_data.html", context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['Cashier'])
def data_table(request, date):
    #03-2020
    month = date[:2]
    year = date[3:]

    orders = Order.objects.filter(order_date__month = month, order_date__year = year, complete=True)
    context = {"orders":orders, "date":date}
 
    return render(request, "cashier/data_table.html", context)

def export_excel(request, date):
    month = date[:2]
    year = date[3:]

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{date}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Monthly Revenue')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Order ID', 'Order Date Time', 'Payment Method', 'Order Total']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = []
    orders = Order.objects.filter(order_date__month = month, order_date__year = year, complete=True)

    for order in orders:
        rows.append((order.id, order.order_date.strftime("%m/%d/%Y, %H:%M:%S"), order.payment_method, order.overall_total))

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response
    
# JSON RESPONSE
def change_status(request):
    data = json.loads(request.body)
    status = data['status']
    orderId = data['order']
    
    order = Order.objects.get(id=orderId)
    status = OrderStatus.objects.get(status=status)

    order.order_status = status
    order.save()

    return JsonResponse("Status Changes", safe=False)

def adjust_quantity_action(request):
    data = json.loads(request.body)
    quantities = data['quantities']
    
    for itemId in quantities:
        item = Item.objects.get(id=itemId)
        item.stock = quantities[itemId]
        item.save()

    messages.success(request, "Quantities have been updated.")
    return JsonResponse("Status Changed", safe=False)

def change_driver(request):
    data = json.loads(request.body)
    driver = data['driver']
    orderId = data['order']

    order = Order.objects.get(id=orderId)
    driver = Driver.objects.get(name=driver)
    order.driver = driver
    order.save()

    # Create delivery
    Delivery.objects.create(customer=order.customer, order=order, driver=driver)
    return JsonResponse("Driver Changed", safe=False)