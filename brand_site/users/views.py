from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView, FormView, UpdateView
from .forms import NewUserForm, ProfileForm
from .models import NewUser, Profile, Order, Favorite
from product.models import Product
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView





class RegForm(CreateView):
    model = NewUser
    form_class = NewUserForm
    template_name = 'registration/registration.html'
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['phone_number'] = ''
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.instance

        profile = Profile.objects.create(user=new_user, first_name=form.cleaned_data['first_name'], user_id=new_user.id)
        # order = Order.objects.create(profile=profile, profile_id=profile.id)
        return response


class ProfileView(TemplateView):
    model = Profile
    template_name = 'profile.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        user = self.request.user
        product = Product.objects.all() 
        profile = Profile.objects.get(user_id=user.id)
        orders = Order.objects.filter(profile_id=profile.id)
        favorites = Favorite.objects.filter(user_id=user.id)

        data['product'] = product
        data['profile'] = profile
        data['orders'] = orders
        data['favorites'] = favorites
        data['user'] = user
        return data


class EditProfile(FormView):
    template_name = 'edit_profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('users:profile_page')

    def form_valid(self, form):
        user = self.request.user
        profile = get_object_or_404(Profile, user_id=user.id)
        form.instance.pk = profile.pk 
        form.instance.user = user 
        form.save()
        return redirect(self.get_success_url())
    

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['yandex_pay'] = ''
        initial['tinkoff_pay'] = ''
        initial['card_field'] = ''
        return initial


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change-password.html'
    form_class = PasswordChangeForm

    def get_form(self):
        form = super().get_form()
        form.user = self.request.user
        return form
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PasswordSuccessView(TemplateView):
    template_name = 'password-success.html'


class PasswordReset(PasswordResetView):
    template_name = 'password-forgot.html'


class PasswordResetSuccessView(TemplateView):
    template_name = 'password-reset-info.html'
    




    








    






