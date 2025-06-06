from typing import Optional
from django.db import transaction
from django.db.models.fields import URLField

from accounts.models import CustomUser
from .models import Website

class WebsiteService:
    """
    Manages Website model
    """

    def __init__(self, user: CustomUser):
        self.user = user

    @transaction.atomic
    def create(self, title: str, url: URLField, username: Optional[str] = None, password: Optional[str] = None) -> Website:
        obj = Website(
            title = title,
            url = url,
            username = username,
            password = password
        )

        obj.full_clean()
        obj.save()

        return obj
