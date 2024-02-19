from typing import Any, Dict
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, FormView, UpdateView
from .forms import NewUserForm, ProfileForm, ProfileChangeForm
from .models import NewUser, Profile, Order, Favorite
from product.models import Product
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from utils.utils import UtilitiesFunctions





class RegForm(CreateView):
    model = NewUser
    form_class = NewUserForm
    template_name = 'registration/registration.html'
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['phone_number'] = ''
        initial['email_field'] = ''
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.instance
        date_of_birth = str(form.cleaned_data['date_of_birth'])

        Profile.objects.create(user=new_user, first_name=form.cleaned_data['first_name'], date_of_birth=date_of_birth, user_id=new_user.id)
        
        return response


class ShowProfile(FormView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = '/'
    model = Profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user.id)

        utilities_object = UtilitiesFunctions(self.request.user)
        
        data['profile'] = utilities_object.get_user_profile()
        data['current_bonuses'] = utilities_object.get_current_bonuses()
        data['future_bonuses'] = utilities_object.future_balls()
        data['aroma_balls'] = utilities_object.get_aroma_balls()
        data['loyal_status'] = utilities_object.get_loyal_status()
        data['orders'] = profile.orders.all()
        return data

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user.id) 
        
        initial['last_name'] = profile.last_name
        
        initial['first_name'] = profile.first_name
        
        initial['phone_number'] = user.phone_number

        initial['email_field'] = user.email_for_reset
        
        initial['date_of_birth'] = profile.date_of_birth

        initial['city'] = profile.city

        initial['index'] = profile.index

        initial['street'] = profile.street

        initial['house'] = profile.house

        initial['corp'] = profile.corp

        initial['room'] = profile.room

        return initial


class EditProfile(UpdateView):
    template_name = 'edit_profile.html'
    form_class = ProfileChangeForm
    success_url = reverse_lazy('users:profile')
    model = Profile

    # мы возвращаем профиль пользователя, связанный с текущим залогиненным пользователем.
    # это необходимо, так как метод предоставляет сам объект для использования в представлении.
    # а в ссылке мы всего лишь ссылаемся на него pk=user.pk.
    def get_object(self):
        return self.request.user.user_profile

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = self.request.user
        user.email_for_reset = form.cleaned_data['email_field']
        user.save()
        form.save()
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        user = self.request.user
        initial['email_field'] = user.email_for_reset
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
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not NewUser.objects.filter(email_for_reset=email).exists():
            return redirect('users:error_message') 
        return redirect('users:password-reset-info')


class ErrorMessage(TemplateView):
    template_name = 'not-exists-email.html'


class QuestionView(TemplateView):
    template_name = 'question.html'

    

        
    
    
    




    








    






