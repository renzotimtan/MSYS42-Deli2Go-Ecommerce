from django.urls import path, include
from . import views

urlpatterns = [
    path('shop/', views.shop, name="shop"),
    path('item/<str:pk>/', views.view_item, name="view-item")
]