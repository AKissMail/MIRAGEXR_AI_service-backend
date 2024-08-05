from django.urls import path
from . import views
"""
URL settings for authentication app, but the main setting is in cfhome/urls.py
"""
urlpatterns = [
    path('', views.authentication)
]
