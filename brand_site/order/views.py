from typing import Any
from django.core.exceptions import ValidationError
from django.http import *
from django.shortcuts import render
from django.views.generic import *
from utils.utils import UtilitiesFunctions
from users.models import *
from cart.cart import Cart
from .forms import NewUserForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
from django.shortcuts import redirect


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderPay(CreateView):
    model = Order
    form_class = NewUserForm
    template_name = 'payment.html'
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        utilities_object = UtilitiesFunctions(self.request.user)
        profile = Profile.objects.get(user=self.request.user.id)
        total_price = int(cart.get_total_price()) + 199
        birthday_price = utilities_object.birthday_discount(int(cart.get_total_price()))
        data['cart'] = cart
        data['total_bonuses'] = utilities_object.showing_income_balls(int(cart.get_total_price()))
        data['current_bonuses'] = int(profile.current_bonuses)
        data['total_price'] = total_price 
        # либо всю стоимость, либо стоимость скидки
        data['birthday_discount'] = total_price - birthday_price
        # либо 0, либо стоимость заказа с учетом скидки
        data['birthday_price'] = birthday_price + 199
        return data


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'making.html'

    # def form_valid(self, form):
    #     PRODUCTS_LIST = []
    #     profile = Profile.objects.get(user=self.request.user.id)
    #     order_data = form.cleaned_data # {'city': 'Москва', 'index': '105523', 'street': '15-я парковая', 'corp': '1', 'house': '54', 'room': '52', 'shipment_date': '15.02.2024', 'promo': '', 'current_bonuses': '17599'}
        
    #     city = order_data['city']
    #     index = order_data['index']
    #     street = order_data['street']
    #     corp = order_data['corp']
    #     house = order_data['house']
    #     room = order_data['room']
    #     shipment_date = order_data['shipment_date']
    #     promo = order_data['promo']
    #     current_bonuses = order_data['current_bonuses']

    #     cart = Cart(self.request)
    #     products = cart.get_content()
    #     for product in products:
    #         parfume = Product.objects.get(id=product[0])
    #         PRODUCTS_DICT = {
    #             f"http://127.0.0.1:8000{parfume.get_absolute_url()}": f"{product[1]['quantity']} шт.",
    #         }
    #         PRODUCTS_LIST.append(PRODUCTS_DICT)
        
        # print(f"\n\nЗапрошенные бонусы:\n{order_data['current_bonuses']}\nФормат: {type(order_data['current_bonuses'])}\nНовый формат: {0 if ' ' else int(order_data['current_bonuses'])}\n\nТекущие бонусы:\n{profile.current_bonuses}\nФормат: {profile.current_bonuses}\nНовый формат: {int(profile.current_bonuses)}\n\n")
        # try:
        #     inputed_bonuses = 0 if ' ' else int(order_data['current_bonuses'])
        #     if inputed_bonuses > int(profile.current_bonuses):
        #         raise ValidationError("Недостаточно бонусов для получения скидки!")

        # except ValueError:
        #     raise ValidationError("Недостаточно бонусов для получения скидки!")
        
        # if not (order_data['promo'] in PromoCode.objects.all()):
        #     raise ValueError
        
        # else:
        #     order = Order (
        #         profile=profile,
        #         product=PRODUCTS_LIST,
        #         city=
                
        #     )

        # order_instance = Order(
        #     field1=order_data['field1'],
        #     field2=order_data['field2'],
        # )

        # order_instance.save()

        # return redirect(reverse('order:check-bonuses'))




    
    # def get(self, request):
    #     form = OrderForm(request.POST)
    #     current_bonuses = request.POST.get('current_bonuses')
    #     print(f"\nЗапрошенные бонусы: {current_bonuses}\n")
    #     return HttpResponse()
        # if form.is_valid():
        #     order = form.save(commit=False)
        #     profile = Profile.objects.get(user=self.request.user.id)
        #     Order.objects.create(profile=profile)
        #     return redirect(reverse('order:order-pay'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        utilities_object = UtilitiesFunctions(self.request.user)
        profile = Profile.objects.get(user=self.request.user.id)
        total_price = int(cart.get_total_price()) + 199
        birthday_price = utilities_object.birthday_discount(int(cart.get_total_price()))
        data['cart'] = cart
        data['total_bonuses'] = utilities_object.showing_income_balls(int(cart.get_total_price()))
        data['current_bonuses'] = int(profile.current_bonuses)
        data['total_price'] = total_price 
        data['birthday_discount'] = total_price - birthday_price
        data['birthday_price'] = birthday_price + 199
        return data

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user.id)   
        shipment_date = datetime.now().date() + timedelta(days=2)  
        initial['city'] = profile.city   
        initial['index'] = profile.index
        initial['street'] = profile.street
        initial['house'] = profile.house
        initial['corp'] = profile.corp
        initial['room'] = profile.room
        initial['shipment_date'] = shipment_date.strftime('%d.%m.%Y')

        return initial


def check_bonuses(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user.id)
        current_bonuses = int(profile.current_bonuses)

        print(f"\n{request.POST.get('input_data')}\n")

        try:
            input_bonuses = int(request.POST.get('input_data'))
        except TypeError:
            input_bonuses = 0

        if input_bonuses > current_bonuses:
            return JsonResponse({'success': False, 'message': 'Число запрошенных бонусов больше текущих!'})
        else:
            return JsonResponse({'success': True})
    

