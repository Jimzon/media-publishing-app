from rest_framework import serializers

from company_publishing.companies.models import Company
from company_publishing.users.api.serializers import EmbeddedUserSerializer


class CompanySerializer(serializers.ModelSerializer):
    created_by = EmbeddedUserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
