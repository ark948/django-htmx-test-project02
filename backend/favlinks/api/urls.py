from django.urls import path

from . import views

urlpatterns = [
    path("websites/list/", views.WebsiteView.as_view(), name='api-website-list'),
    path('', views.api_index, name='api-index'),
]