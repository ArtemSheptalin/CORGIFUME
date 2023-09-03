from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import NewUserForm
from .models import NewUser, Profile
from product.models import Product
from .models import Profile


class RegForm(CreateView):
    model = NewUser
    form_class = NewUserForm
    template_name = 'registration/registration.html'
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['phone_number'] = ''
        return initial


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        product = Product.objects.all() 
        profile = self.request.user.profile
        data['product'] = product
        data['profile'] = profile
        return data
    






