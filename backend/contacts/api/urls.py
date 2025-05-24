from django.urls import path, include

from . import views
from .routers import router

urlpatterns = [
    path("list/", views.ContactsListView.as_view(), name='api_list'),
    path('', views.APIIndexView.as_view(), name='api_index')
]


# Routers
urlpatterns += [
    path('set/', include(router.urls))
]