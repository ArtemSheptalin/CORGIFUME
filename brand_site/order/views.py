from typing import Any
from django.shortcuts import render
from django.views.generic import CreateView
from users.models import Order
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


@method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
class OrderCreate(CreateView):
    model = Order
    form_class = NewUserForm
    template_name = 'order.html'
    success_url = '/'

    

