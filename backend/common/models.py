"""Shared abstract models.

Domain models inherit from these instead of repeating UUID and timestamp
fields. UUID primary keys keep sequential record counts out of public URLs;
timestamps are UTC and immutable on creation.
"""

from __future__ import annotations

import uuid

from django.db import models


class UUIDPrimaryKeyModel(models.Model):
    """Model whose primary key is an opaque UUID."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """Adds creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(UUIDPrimaryKeyModel, TimeStampedModel):
    """Standard base for platform records."""

    class Meta(UUIDPrimaryKeyModel.Meta):
        abstract = True
        ordering = ("-created_at",)
