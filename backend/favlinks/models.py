from django.db import models

from encrypted_fields.fields import EncryptedCharField

from accounts.models import CustomUser

# Create your models here.


class Website(models.Model):
    title = models.CharField(verbose_name="Title", max_length=25, null=True, blank=True)
    url = models.URLField(verbose_name="Address", unique=True, null=False, blank=False)
    username = models.CharField(verbose_name="Username", max_length=68, null=True, blank=True)
    password = EncryptedCharField(verbose_name="Password", null=True, blank=True)
    user = models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name='websites') # user.websites.all()

    class Meta:
        verbose_name_plural = "Websites"

    def __str__(self) -> str:
        if self.title:
            return f"[{self.title}]"
        else:
            return f"[{self.url}]"



class Link(models.Model):
    url = models.URLField(verbose_name="Address", null=False, blank=False)
    description = models.CharField(verbose_name="Description", null=True, blank=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='links') # website.links.all()

    class Meta:
        verbose_name_plural = "Links"

    def __str__(self) -> str:
        if self.description:
            return self.description
        else:
            return None