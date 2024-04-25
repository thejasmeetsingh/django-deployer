import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        db_index=True,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
