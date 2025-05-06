from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('delete/<int:pk>/', views.delete_contact, name='delete'),
    path('new/', views.new_contact, name='new-item'),
    path('item-edit/<int:pk>/', views.contact_edit, name='item-edit'),
    path('item-detail/<int:pk>/', views.contact_item, name='item-detail'),
    path('list/', views.contacts_list, name='list'),
    path('', views.index, name='index'),
] + views.ContactView.get_urls()


# path("list/", views.ContactsListView.as_view(), name="list"),