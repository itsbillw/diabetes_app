"""Defines url patterns for users."""

from django.urls import path
from django.contrib.auth.views import login

from . import views

app_name = 'users'
urlpatterns = [
    # Login page.
    path(r'login/', login, {'template_name': 'users/login.html'}, name='login'),

    # Logout page.
    path(r'logout/', views.logout_view, name='logout'),

    # Registration page.
    path(r'register/', views.register, name='register'),
]
