from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.ContactsListView.as_view(), name='api_list'),
    path('', views.APIIndexView.as_view(), name='api_index')
]