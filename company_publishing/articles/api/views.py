import django_filters.rest_framework
from rest_framework import filters, viewsets

from company_publishing.articles.api.serializers import ArticleSerializer
from company_publishing.articles.models import Article
from company_publishing.articles.permissions import ArticlePermission


class ArticleViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [ArticlePermission]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ["status"]
    ordering_fields = ["created_date", "updated_date", "published_date"]
    ordering = ["-created_date"]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
