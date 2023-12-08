from rest_framework import serializers

from company_publishing.articles.models import Article
from company_publishing.users.api.serializers import EmbeddedUserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    writer = EmbeddedUserSerializer(read_only=True)
    editor = EmbeddedUserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {
            "slug": {"read_only": True},
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

    def save(self, **kwargs):
        status = self.validated_data.get("status")
        if self.instance and not self.instance.is_published and status == Article.Status.PUBLISHED:
            self.instance.publish(self.context["request"].user.id)

        return super().save(**kwargs)
