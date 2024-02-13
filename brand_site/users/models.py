from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import *
from django.contrib.postgres.fields import ArrayField

from product.models import Product
import random
from django.utils import timezone
from datetime import date


class CustomAccountManager(BaseUserManager):

    def create_user(self, phone_number, password, **other_fields):

        if not phone_number:
            raise ValueError(_('Это обязательное поле, введите номер телефона!'))

        user = self.model(phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        
        return self.create_user(phone_number, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    
    phone_number = models.CharField(_('Мобильный телефон'), max_length=19, unique=True)
    email_for_reset = models.EmailField(_('Адрес электронной почты'), null=True, unique=True)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'phone_number'
    EMAIL_FIELD = 'email_for_reset'

    
    def __str__(self):
        return f"{self.phone_number}"


class Profile(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, related_name='user_profile')
    date_of_register = models.DateField(default=date.today)
    # Личные данные
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    index = models.CharField(max_length=200, null=True, blank=True)
    house = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    room = models.CharField(max_length=200, null=True, blank=True)
    corp = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.CharField(null=True, blank=True)
    # Программа лояльности
    current_bonuses = models.FloatField(default=0.0)
    future_bonuses = models.IntegerField(default=0)
    aroma_balls = models.IntegerField(default=1) 
    loyal_status = models.CharField(default='Новичок')
    has_birthday_present = models.BooleanField(default=False)
    # платёжные данные
    yandex_pay = models.BigIntegerField(default=0) 
    tinkoff_pay = models.BigIntegerField(default=0)
    card_field = models.BigIntegerField(default=0)

    def formatted_card(self):
        card = str(self.card_field)
        formatted_card = ' '.join(card[i:i+4] for i in range(0, len(card), 4))
        return formatted_card

    def __str__(self):
        return f"{self.user.id}"


class Favorite(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='favorites')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.item}'


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

    city = models.CharField(max_length=200, null=True, blank=True)
    index = models.CharField(max_length=200, null=True, blank=True)
    house = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    room = models.CharField(max_length=200, null=True, blank=True)
    corp = models.CharField(max_length=200, null=True, blank=True)
    order_price = models.FloatField(default=0.0)
    loyal_status = models.CharField(default='Новичок')


class PromoCode(models.Model):
    
    title = models.CharField(max_length=8)
    expiration_date = models.DateField()
    active = models.BooleanField(default=True)
    # category + profile


    def __str__(self):
        return self.title

