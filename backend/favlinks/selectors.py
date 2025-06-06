from typing import Iterable
from django.db.models.query import Q
from .models import Website

def website_list(*, user_id: int) -> Iterable[Website]:
    query = Q(user = user_id)
    return Website.objects.filter(query)