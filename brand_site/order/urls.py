from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'order'

urlpatterns = [
    path('order-pay/', OrderPay.as_view(), name='order-pay'),
    path('order-create/', OrderCreate.as_view(), name='order-create'),
    path('check-bonuses/', check_bonuses, name='check_bonuses'),
    path('tinkoff-kassa/', TinkoffPay.as_view(), name='tinkoff_pay'),
]