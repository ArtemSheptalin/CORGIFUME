from django.contrib import admin
from django.urls import path, include
from main_application.views import MainPageView
from .views import RegForm

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', MainPageView.as_view(), name='main_page'),
    path('reg/', RegForm.as_view(), name='registration_page'),
]