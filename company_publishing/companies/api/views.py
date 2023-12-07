import django_filters.rest_framework
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from company_publishing.companies.api.serializers import CompanySerializer
from company_publishing.companies.models import Company


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ["status"]
    ordering_fields = ["name", "created_date", "updated_date"]
    ordering = ["name"]

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
