from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Company Publishing.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class Type(models.TextChoices):
        EDITOR = "editor", _("Editor")
        WRITER = "writer", _("Writer")

    first_name = None  # type: ignore
    last_name = None  # type: ignore

    # First and last name do not cover name patterns around the globe
    image = models.ImageField(upload_to="users", blank=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    type = TextField(choices=Type.choices, default=Type.EDITOR)
    added_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def is_editor(self) -> bool:
        return self.type == self.Type.EDITOR
