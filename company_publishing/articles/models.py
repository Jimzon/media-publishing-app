from django.db import models


class Article(models.Model):
    class Status(models.TextChoices):
        FOR_EDIT = "for_edit", "For Edit"
        PUBLISHED = "published", "Published"

    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="articles")
    title = models.TextField()
    body = models.TextField()
    status = models.TextField(choices=Status.choices, default=Status.FOR_EDIT)
    writer = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="written_articles")
    editor = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, related_name="edited_articles", blank=True, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)
