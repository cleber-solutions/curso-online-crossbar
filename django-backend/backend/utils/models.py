from django.db import models
import ulid

from powerlibs.django.contrib.models import TimestampedModelMixin


def ulid_str_generator():
    return ulid.new().str


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.CharField(max_length=26, default=ulid_str_generator,
                          primary_key=True, editable=False)


class TimestampedOwnedModelMixin(TimestampedModelMixin):
    class Meta:
        abstract = True

    created_by = models.ForeignKey('auth.User')
    updated_by = models.ForeignKey('auth.User')
