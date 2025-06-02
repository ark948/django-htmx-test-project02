from django.urls import path

from . import views

urlpatterns = [
    path("website/item/<int:pk>/", views.WebsiteDetails.as_view(), name='api-website-item'),
    path("websites/list/", views.WebsiteView.as_view(), name='api-website-list'),
    path('', views.api_index, name='api-index'),
]