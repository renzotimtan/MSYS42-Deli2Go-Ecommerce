from django.urls import path, include
from . import views

urlpatterns = [
    path('add-order', views.add_order, name="add-order"),
]
