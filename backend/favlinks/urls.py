from django.urls import path, include

from . import views

app_name = 'favlinks'

urlpatterns = [
    path("api/", include('favlinks.api.urls')),
    path('', views.index, name='index'),
]