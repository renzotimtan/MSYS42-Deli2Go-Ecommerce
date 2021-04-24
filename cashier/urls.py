from django.urls import path, include
from . import views

urlpatterns = [
    # Crud Items
    path('add-items/', views.add_items, name="add-items"),
    path('edit-items/<str:pk>/', views.edit_items, name="edit-items"),
    path('delete-items/', views.delete_items, name="delete-items"),
    path('adjust-quantity/', views.adjust_quantity, name="adjust-quantity"),
    path('adjust-quantity-action/', views.adjust_quantity_action, name="adjust-quantity-action"),

    # Dashboard
    path('edit-inventory/', views.edit_inventory, name="edit-inventory"),
    path('customer-orders/', views.customer_orders, name="customer-orders"),
    path('change-status/', views.change_status, name="change-status")
]
