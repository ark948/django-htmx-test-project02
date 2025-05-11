from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('compound-serach/', views.compound_search, name='compound'),
    path('phone-number-search/', views.search_within_contacts_phone_number, name='phone-search'),
    path('email-search/', views.search_within_contacts_emails, name='email-search'),
    path('export/', views.export_csv, name='export'),
    path('import/', views.import_csv, name='import'),
    path('item-edit/<int:pk>/', views.contact_edit, name='item-edit'),
    path('item-detail/<int:pk>/', views.contact_item, name='item-detail'),
    path('list/', views.contacts_list, name='list'),
    path('', views.index, name='index'),

    # Removed paths
    # path('new/', views.new_contact, name='new-item'),
    # path('delete/<int:pk>/', views.delete_contact, name='delete'),
]


# New revised routes
urlpatterns += [
    path('revised/new-contact/', views.new_contact_v2, name='new'),
    path('revised/delete-contact/<int:pk>/', views.delete_contact_v2, name='delete')
]

# Django Neapolitan, could act as a backup, maybe
urlpatterns += views.ContactView.get_urls()
