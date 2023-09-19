from django.contrib import admin
from django.urls import path, include
from .views import OrderCreate

app_name = 'order'

urlpatterns = [
    path('order-create/', OrderCreate.as_view(), name='order-create'),
]