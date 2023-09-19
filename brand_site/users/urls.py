from django.contrib import admin
from django.urls import path, include
from main_application.views import MainPageView
from .views import RegForm, ProfileView, EditProfile, PasswordChange, PasswordSuccessView, PasswordReset, PasswordResetSuccessView
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', MainPageView.as_view(), name='main_page'),
    path('reg/', RegForm.as_view(), name='registration_page'),
    path('profile/', ProfileView.as_view(), name='profile_page'),
    path('edit-profile/', EditProfile.as_view(), name='edit-profile'),
    path('change-password/', PasswordChange.as_view(success_url=reverse_lazy('users:password-success')), name='password_change_lk'),
    path('password-success/', PasswordSuccessView.as_view(), name='password-success'),
    path('password-reset/', PasswordReset.as_view(success_url=reverse_lazy('users:password-reset-info')), name='password_reset_lk'),
    path('password-reset-success/', PasswordResetSuccessView.as_view(), name='password-reset-success'),
]