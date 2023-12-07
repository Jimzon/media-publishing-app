from rest_framework import serializers

from company_publishing.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        extra_kwargs = {"created_by": {"read_only": True}}
