from django.shortcuts import render
from django.views.generic import CreateView
from .forms import NewUserForm
from .models import NewUser



class RegForm(CreateView):
    model = NewUser
    form_class = NewUserForm
    template_name = 'registration/registration.html'
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['phone_number'] = ''
        return initial



