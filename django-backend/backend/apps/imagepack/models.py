from django.contrib.auth.models import User
from django.db import models

from utils.models import BaseModel, TimestampedOwnedMixin


class ImagePack(BaseModel, TimestampedOwnedMixin):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=32, default='new', blank=True)
    status_message = models.CharField(max_length=128, null=True, blank=True)
