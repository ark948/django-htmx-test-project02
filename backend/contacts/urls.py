from django.urls import path, include

from . import views

app_name = 'contacts'

urlpatterns = [
    path('api/', include("contacts.api.urls")),
    path('compound-serach/', views.compound_search, name='compound'),
    path('phone-number-search/', views.search_within_contacts_phone_number, name='phone-search'),
    path('import/', views.import_csv, name='import'),
    path('item-detail/<int:pk>/', views.contact_item, name='item-detail'),
    path('list/', views.contacts_list, name='list'),
    path('', views.index, name='index'),
]


# New revised routes
urlpatterns += [
    path('email-search-results-export/', views.export_email_search_results, name='export-selected-emails'),
    path('email-search/', views.search_within_contacts_emails_v2, name='email-search'),
    path('revised/export/', views.export_csv_v2, name='export'),
    path('revised/new-contact/', views.new_contact_v2, name='new'),
    path('revised/delete-contact/<int:pk>/', views.delete_contact_v2, name='delete'),
    path('revised/edit-contact/<int:pk>/', views.contact_edit_v2, name='edit'),
    path('api/', include('contacts.api.urls'))
]

# Django Neapolitan, could act as a backup, maybe
urlpatterns += views.ContactView.get_urls()
