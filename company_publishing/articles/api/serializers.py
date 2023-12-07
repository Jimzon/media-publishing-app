from django.utils import timezone
from rest_framework import serializers

from company_publishing.articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {
            "slug": {"read_only": True},
            "writer": {"read_only": True},
            "editor": {"read_only": True},
            "published_date": {"read_only": True},
        }

    def validate_status(self, value):
        publish = value == Article.Status.PUBLISHED

        if self.instance:
            if not publish and self.instance.is_published:
                raise serializers.ValidationError("Cannot unpublish an article")
            if publish and not self.context["request"].user.is_editor:
                raise serializers.ValidationError("Only editors can publish articles")

        elif publish:
            raise serializers.ValidationError("Cannot publish a new article")

        return value

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.instance and data.get("status") == Article.Status.PUBLISHED:
            if not self.instance.is_published:
                data["published_date"] = timezone.now()
        return data
