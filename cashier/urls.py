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
    path('change-status/', views.change_status, name="change-status"),
    path('view-proof/', views.view_proof, name="view-proof"),
    path('view-proof-picture/<str:pk>/', views.view_proof_picture, name="view-proof-picture"),
    path('handle-proof/<str:pk>/<str:action>/', views.handle_proof, name="handle-proof"),
    path('add-driver/', views.add_driver, name="add-driver"),
    path('change-driver/', views.change_driver, name="change-driver"),
    path('export-data/', views.export_data, name="export-data"),
    path('data-table/<str:date>/', views.data_table, name="data-table"),
    path('export-excel/<str:date>/', views.export_excel, name="export-excel")
]
