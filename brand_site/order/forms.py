from django import forms
from users.models import Order

class NewUserForm(forms.ModelForm):

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
        

