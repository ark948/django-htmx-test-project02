from django.db import models

from accounts.models import CustomUser

# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=80, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=30)
    address = models.TextField(verbose_name="Address", max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name='contacts' ) # user.contacts.all() 

    class Meta:
        unique_together = ('user', 'email')
        ordering = ['created_at']
        verbose_name_plural = "Contacts"

    @property
    def full_name(self) -> str:
        return self.first_name + self.last_name

    def __str__(self) -> str:
        return f"[{self.full_name} <{self.email}>]"