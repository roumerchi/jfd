from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

"""
class ContactStatusChoices(models.IntegerChoices):
    DEFAULT = 0, 'default'
    BLOCKED = 1, 'blocked'
"""

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=False, default=uuid4, editable=False, unique=True)

    def __str__(self): # remove?
        return self.username

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Contacts(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='contacts') # do nothing bcs in reality it works similar
    status = models.ForeignKey("ContactStatus", on_delete=models.PROTECT, related_name='contacts')
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    phone = PhoneNumberField(unique=True, region='PL', blank=False, null=False)
    email = models.EmailField(blank=True, unique=True)
    city = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['last_name']
        indexes = [
            models.Index(fields=['last_name']),
            models.Index(fields=['created_at']),
        ]


class ContactStatus(models.Model): # basic statuses ['default', 'blocked'] are set in the initialization command
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'contact_status'
        verbose_name = 'Contact status'
        verbose_name_plural = 'Contact statuses'

    def __str__(self):
        return self.title
