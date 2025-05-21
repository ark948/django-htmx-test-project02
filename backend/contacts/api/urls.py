from django.urls import path

from . import views

urlpatterns = [
    path('', views.APIIndexView.as_view(), name='api_index')
]