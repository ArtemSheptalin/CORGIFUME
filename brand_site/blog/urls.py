from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'blog'

urlpatterns = [
    path('corgifume-posts/', Blog.as_view(), name='blog'),
]