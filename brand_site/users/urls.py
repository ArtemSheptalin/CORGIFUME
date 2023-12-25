from django.contrib import admin
from django.urls import path, include
from main_application.views import MainPageView
from .views import *
from django.urls import reverse_lazy

from django.contrib.auth.views import PasswordResetDoneView

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', MainPageView.as_view(), name='main_page'),
    path('reg/', RegForm.as_view(), name='registration_page'),
    path('profile/', ShowProfile.as_view(), name='profile'),
    path('edit-profile/<int:pk>/', EditProfile.as_view(), name='edit_profile'),
    path('change-password/', PasswordChange.as_view(success_url=reverse_lazy('users:password-success')), name='password_change_lk'),
    path('password-success/', PasswordSuccessView.as_view(), name='password-success'),
    path('password-reset/', PasswordReset.as_view(), name='password_reset_lk'),
    path('password-reset-success/', PasswordResetDoneView.as_view(template_name='password-reset-info.html'), name='password-reset-info'),
    path('error-reset/', ErrorMessage.as_view(), name='error_message'),
    path('question/', QuestionView.as_view(), name='question'),
]