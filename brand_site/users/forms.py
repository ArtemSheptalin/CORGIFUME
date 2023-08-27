from django.contrib.auth.forms import forms, UserCreationForm
from .models import NewUser
from .validators import check_phone_number, check_email
from django.utils.translation import gettext_lazy as _
import re


class NewUserForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, validators=[check_phone_number])
    email_field = forms.CharField(required=True)
    first_name = forms.CharField(max_length=10, required=True)

    class Meta:
        model = NewUser
        fields = ('phone_number', 'email_field', 'first_name', 'password1', 'password2')