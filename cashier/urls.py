from django.urls import path, include
from . import views

urlpatterns = [
    path('add-items', views.add_items, name="add-items"),
]
