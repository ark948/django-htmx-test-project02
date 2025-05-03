from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('item-detail/<int:pk>/', views.contact_item, name='item-detail'),
    path("list/", views.ContactsListView.as_view(), name="list"),
    path('', views.index, name='index'),
] + views.ContactView.get_urls()