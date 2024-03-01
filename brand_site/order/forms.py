from django import forms
from users.models import *
from order.models import *

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
    city = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'city_ID'}))
    index = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'index_ID'}))
    street = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'street_ID'}))
    corp = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'corp_ID'}))
    house = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'house_ID'}))
    room = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'room_ID'}))
    shipment_date = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'shipment_date_ID'}))
    promo = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'promo_formID'}))
    current_bonuses = forms.CharField(max_length=10000, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'bonuses_formID'}))
    comment = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'class': 'delivery__input', 'id': 'comment_ID'}))

    class Meta:
        model = Profile
        fields = []
    

class BonusesUse(forms.ModelForm):
    class Meta:
        model = Profile
        fields =[
            'current_bonuses',
        ]


class PaymentForm(forms.Form):
    terminalkey = forms.CharField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'type': 'hidden', 'name': '1708362189241DEMO', 'value': '1708362189241DEMO'}))
    frame = forms.CharField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'type': 'hidden', 'name': 'frame', 'value': 'false'}))
    language = forms.CharField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'type': 'hidden', 'name': 'language', 'value': 'ru'}))
    reciept = forms.CharField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'type': 'hidden', 'name': 'receipt', 'value': ''}))
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'placeholder': 'Сумма заказа', 'readonly': 'true', 'required': 'true'}))
    order_number = forms.CharField(widget=forms.TextInput(attrs={"class": "payform-tinkoff-row", "type": "hidden", "placeholder": "Номер заказа", "name": "order"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"class": "payform-tinkoff-row", "type": "hidden", "placeholder": "Описание заказа", "name": "description"}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'placeholder': 'ФИО плательщика', 'readonly': 'true'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'placeholder': 'E-mail', 'readonly': 'true', 'required': 'true'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'payform-tinkoff-row', 'placeholder': 'Контактный телефон', 'readonly': 'true'}))    


        

