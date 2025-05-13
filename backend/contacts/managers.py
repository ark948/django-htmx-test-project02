from django.db.models import QuerySet, Manager


# not used
class ContactModelCustomManager(Manager):
    pass


class ContactModelCustomQuerySet(QuerySet):

    def get_total_contacts(self) -> int:
        return len(self.all())