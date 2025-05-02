from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.index, name='index'),
    path("list/", views.ContactsListView.as_view(), name="list"),
] + views.ContactView.get_urls()