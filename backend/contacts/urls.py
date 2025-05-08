from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('export/', views.export_csv, name='export'),
    path('import/', views.import_csv, name='import'),
    path('delete/<int:pk>/', views.delete_contact, name='delete'),
    path('new/', views.new_contact, name='new-item'),
    path('item-edit/<int:pk>/', views.contact_edit, name='item-edit'),
    path('item-detail/<int:pk>/', views.contact_item, name='item-detail'),
    path('list/', views.contacts_list, name='list'),
    path('', views.index, name='index'),
]


# Django Neapolitan, could act as a backup, maybe
urlpatterns += views.ContactView.get_urls()
