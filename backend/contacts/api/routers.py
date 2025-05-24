from rest_framework import routers


from . import views


router = routers.SimpleRouter()
# http://127.0.0.1:8000/contacts/api/set/list/
router.register(r'list', views.ContactsViewSet, basename='api_contacts')