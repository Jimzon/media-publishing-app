from django.db import models


class Company(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"

    name = models.TextField()
    status = models.TextField(choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        constraints = [models.UniqueConstraint(fields=["name", "created_by"], name="unique_company_name")]

    def __str__(self):
        return self.name
