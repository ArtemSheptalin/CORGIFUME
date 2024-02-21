from django.db import models
from users.models import *


class PromoCode(models.Model):
    
    profile = models.ManyToManyField(Profile, related_name="promocodes")
    title = models.CharField(max_length=16)
    expiration_date = models.DateField(blank=True, null=True)
    discount = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)
    category_of_usage = models.CharField(null=True, blank=True)
    product_of_usage = models.CharField(null=True, blank=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.title
