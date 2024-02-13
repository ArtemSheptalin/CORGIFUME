from django import forms
from users.models import Order, Profile

class NewUserForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'order_number',
            'order_date',
            'product',
            'order_price',
        ]


class OrderForm(forms.ModelForm):
    shipment_date = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    promo = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input'}))
    current_bonuses = forms.CharField(max_length=10000, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'bonuses_formID'}))

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

        

