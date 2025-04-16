from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
]
