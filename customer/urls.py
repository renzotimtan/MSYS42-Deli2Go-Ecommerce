from django.urls import path, include
from . import views

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('item/<str:pk>/', views.view_item, name="view-item"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update-item"),

    # auth
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    # dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
    path('addresses/', views.addresses, name="addresses"),
    path('add_address/', views.add_address, name="add-address"),
    path('edit_address/<str:pk>/', views.edit_address, name="edit-address"),
    path('delete_address/', views.delete_address, name="delete-address"),
]