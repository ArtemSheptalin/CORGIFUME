from django import forms
from users.models import Order, Profile

class NewUserForm(forms.ModelForm):
    current_bonuses = forms.CharField(max_length=10000, required=False)

    class Meta:
        model = Order
        fields = [
            'name',
            'phone',
            'shipping_address',
            'order_number',
            'order_date',
            'product',
            'order_price',
        ]


class OrderForm(forms.ModelForm):
    shipment_date = forms.CharField(max_length=10, required=False)
    promo = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Profile
        fields = [
            'city',
            'index',
            'street',
            'corp',
            'house',
            'room',
        ]

class BonusesUse(forms.ModelForm):
    class Meta:
        model = Profile
        fields =[
            'current_bonuses',
        ]

        

