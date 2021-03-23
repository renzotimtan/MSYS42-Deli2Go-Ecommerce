from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Cashier)
admin.site.register(Driver)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderedItem)
admin.site.register(Delivery)