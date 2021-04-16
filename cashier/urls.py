from django.urls import path, include
from . import views

urlpatterns = [
    path('add-items/', views.add_items, name="add-items"),
    path('dashboard/', views.dashboard, name="cashier-dashboard"),
    path('edit-inventory/', views.edit_inventory, name="edit-inventory"),
]
