from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, phone_number, first_name, email_field, password, **other_fields):

        if not phone_number:
            raise ValueError(_('Это обязательное поле, введите номер телефона!'))
        
        if not email_field:
            raise ValueError(_('Это обязательное поле, введите адрес электронной почты!'))
        
        if not first_name:
            raise ValueError(_('Как Вас зовут?'))

        email = self.normalize_email(email_field)
        user = self.model(phone_number=phone_number,first_name=first_name, email_field=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number, first_name, email_field, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        
        return self.create_user(phone_number, first_name, email_field, password, **other_fields)



class NewUser(AbstractBaseUser, PermissionsMixin):
    
    phone_number = models.CharField(_('Мобильный телефон'), max_length=15, unique=True)
    email_field = models.EmailField(_('Адрес электронной почты'), unique=True)
    first_name = models.CharField(max_length=50)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomAccountManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email_field', 'first_name']
    
    def __str__(self):
        return f"{self.first_name}: {self.phone_number}"



