"""Platform roles.

Kept in a dependency-free module so permission classes and the user model can
both import it without creating a cycle.
"""

from __future__ import annotations

from django.db import models


class Role(models.TextChoices):
    STUDENT = "student", "Student"
    EMPLOYER = "employer", "Employer"
    UNIVERSITY = "university", "University"
    ADMINISTRATOR = "administrator", "Administrator"
