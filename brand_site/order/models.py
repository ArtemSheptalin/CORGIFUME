from django.db import models
from users.models import *
import random
from django.utils import timezone


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    order_number = models.IntegerField(default=random.randint(100000, 999999), unique=True)
    order_date = models.DateTimeField(default=timezone.now)
    product = models.JSONField(default=list)
    status = models.CharField(max_length=100, choices=(
        ('processing', 'В обработке'),
        ('created', 'Создан'),
        ('accepted', 'Принят'),
        ('completed', 'Доставлено')
    ), default='processing')

    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(max_length=20, null=True, blank=True)
    shipment_type = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    index = models.CharField(max_length=200, null=True, blank=True)
    house = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    room = models.CharField(max_length=200, null=True, blank=True)
    corp = models.CharField(max_length=200, null=True, blank=True)
    shipment_date = models.CharField(max_length=20, null=True, blank=True)
    order_price = models.FloatField(default=0.0)
    loyal_status = models.CharField(default='Новичок')

    def __str__(self):
        return self.order_number
