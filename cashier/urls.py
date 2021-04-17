from django.urls import path, include
from . import views

urlpatterns = [
    # Crud Items
    path('add-items/', views.add_items, name="add-items"),
    path('edit-items/<str:pk>/', views.edit_items, name="edit-items"),
    path('delete-items/', views.delete_items, name="delete-items"),

    # Dashboard
    path('dashboard/', views.dashboard, name="cashier-dashboard"),
    path('edit-inventory/', views.edit_inventory, name="edit-inventory"),
]
