from django.contrib import admin
from django.urls import path, include
from .views import OrderPay, OrderCreate

app_name = 'order'

urlpatterns = [
    path('order-pay/', OrderPay.as_view(), name='order-pay'),
    path('order-create/', OrderCreate.as_view(), name='order-create'),
]