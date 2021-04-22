from django.db import models
from django.contrib.auth.models import User
import datetime

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    mobile_phone = models.CharField(max_length=11)

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name

# class Cashier(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=100)
    
#     def __str__(self):
#         return self.email

class Driver(models.Model):
    name = models.CharField(max_length=80)
    mobile_phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Address(models.Model):
    street_address = models.CharField(max_length=70)
    barangay = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=4)
    home_phone = models.CharField(max_length=8)

    # Foreign Key
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.street_address}, {self.barangay}, {self.city} {self.zip_code}"

class PaymentMethod(models.Model):
    method = models.CharField(max_length=50)

    def __str__(self):
        return self.method

class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

class Order(models.Model):

    order_date = models.DateTimeField(auto_now_add=True)
    receive_date = models.DateField(null=True)
    receive_time = models.TimeField(null=True)
    proof_of_payment = models.ImageField(null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    #ecommerce
    complete = models.BooleanField(default=False)

    # Foreign Keys
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    # cashier = models.ForeignKey(Cashier, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_cart_total(self):
        ordered_items = self.ordereditem_set.all()
        total = sum([item.get_total for item in ordered_items])
        return total

    @property
    def get_overall_total(self):
        ordered_items = self.ordereditem_set.all()
        total = sum([item.get_total for item in ordered_items]) + self.delivery_fee
        return total


    def __str__(self):
        return str(self.pk)

class Category(models.Model):
    name = models.CharField(max_length=44)

    def __str__(self):
        return self.name

class Item(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=500, blank=True)
    brand = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Foreign Keys
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_shortened_desc(self):
        return self.description[0:50]
    
    def __str__(self):
        return self.name

class OrderedItem(models.Model):
    quantity = models.PositiveIntegerField(default=0)

    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total

    def __str__(self):
        return str(self.pk)


class Delivery(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)