from typing import Any
from django.shortcuts import render
from django.views.generic import CreateView
from users.models import Order, Profile
from cart.cart import Cart
from .forms import NewUserForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from datetime import datetime, timedelta


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderPay(CreateView):
    model = Order
    form_class = NewUserForm
    template_name = 'payment.html'
    success_url = '/'


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'making.html'
    success_url = '/'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        data['cart'] = cart
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

    

