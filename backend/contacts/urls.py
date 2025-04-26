from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.index, name='index'),
    path("list/", views.ContactsListView.as_view(), name="list")
]
