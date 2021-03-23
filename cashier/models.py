from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    mobile_phone = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Cashier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    
    def __str__(self):
        return self.email

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

class Order(models.Model):
    PAYMENT_METHOD = (
        ("GCash", "GCash"),
        ("Cash On Delivery", "Cash On Delivery"),
        ("Cash On Pickup", "Cash On Pickup")
    )

    ORDER_STATUS = (
        ("Order Sent", "Order Sent"),
        ("Order Confirmed", "Order Confirmed"),
        ("Payment Sent", "Payment Sent"),
        ("Payment Confirmed", "Payment Confirmed"),
        ("Ready for Pickup", "Ready for Pickup"),
        ("To Be Delivered", "To Be Delivered"),
        ("Order On The Way", "Order On The Way"),
        ("Delivered", "Delivered")
    )

    order_date = models.DateTimeField(auto_now_add=True)
    receive_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS)
    proof_of_payment = models.ImageField(null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2)

    # Foreign Keys
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    cashier = models.ForeignKey(Cashier, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.pk

class Category(models.Model):
    CATEGORY = (
        ("Alcohol and Hygiene", "Alcohol and Hygiene"),
        ("Candy/Gum", "Candy/Gum"),
        ("Canned Drinks/Bottled Drinks/Powdered Drinks", "Canned Drinks/Bottled Drinks/Powdered Drinks"),
        ("Gong Cha", "Gong Cha"),
        ("Magazines", "Magazines"),
        ("Pastries", "Pastries"),
        ("Potato Corner", "Potato Corner"),
        ("Snacks", "Snacks"),
        ("Turks", "Turks")
    )

    name = models.CharField(max_length=44, choices=CATEGORY)

    def __str__(self):
        return self.name

class Item(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500, blank=True)
    brand = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Foreign Keys
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

class OrderedItem(models.Model):
    quantity = models.PositiveIntegerField()

    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.pk


class Delivery(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)