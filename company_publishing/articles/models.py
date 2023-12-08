import random
import string

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Article(models.Model):
    class Status(models.TextChoices):
        FOR_EDIT = "for_edit", "For Edit"
        PUBLISHED = "published", "Published"

    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="articles")
    title = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to="articles", blank=True, null=True)
    status = models.TextField(choices=Status.choices, default=Status.FOR_EDIT)
    writer = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="written_articles")
    editor = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, related_name="edited_articles", blank=True, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # set slug
        if not self.slug:
            random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

            self.slug = slugify(self.title)[:190] + "-" + random_string

        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED

    def publish(self, editor_id):
        self.published_date = timezone.now()
        self.editor_id = editor_id
