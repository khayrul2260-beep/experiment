from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower, Trim

class User(AbstractUser):

    email = models.EmailField(
        blank=True,
        default=""
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        default=""
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower(Trim("email")),
                condition=~Q(email=""),
                name="unique_user_normalized_email"
            )
        ]

    def __str__(self):
        return self.username
