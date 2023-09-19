from django.contrib.auth.forms import forms, UserCreationForm
from .models import NewUser
from .validators import check_phone_number, check_email
from django.utils.translation import gettext_lazy as _
import re
from .models import Profile



class NewUserForm(UserCreationForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'registrationFormDes', 'required': 'true'}))
    password2 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'registrationFormDes', 'required': 'true'}))

    class Meta:
        model = NewUser
        fields = [
            'phone_number', 
            'email_field', 
            'first_name', 
            'password1', 
            'password2'
        ]

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'email_field': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'first_name': forms.TextInput(attrs={'class': 'registrationFormDes'}),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'address',
            'date_of_birth',
            'yandex_pay',
            'tinkoff_pay',
            'card_field',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'last_name': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'address': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'yandex_pay': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'tinkoff_pay': forms.TextInput(attrs={'class': 'registrationFormDes'}),
            'card_field': forms.TextInput(attrs={'class': 'registrationFormDes'}),
        }

        




