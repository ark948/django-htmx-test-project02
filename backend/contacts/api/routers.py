from rest_framework import routers


from . import views


router = routers.SimpleRouter()
# http://127.0.0.1:8000/contacts/api/set/contacts/
router.register(r'contacts', views.ContactsViewSet, basename='api_contacts')