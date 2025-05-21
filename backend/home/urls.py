from django.urls import path, include

from . import views

app_name = 'home'

urlpatterns = [
    path('api/', include('home.api.urls')),
    path('', views.IndexPage.as_view(), name='index'),
]
