from rest_framework import serializers

from ereturns.institutes.models import (
    FinancialInstitute, Branch, Department
)


class BaseFinancialInstituteSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="fi_nm")
    value = serializers.CharField(source="fi_id")

    class Meta:
        model = FinancialInstitute
        fields = ["label", "value"]


class FinancialInstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialInstitute
        fields = ["fi_id", "fi_nm", "fi_alias", "geo_area", "fi_class_id", "fi_status", "financial_institute_type"]


class BaseBranchSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="branch_nm")
    value = serializers.CharField(source="fi_branch_id")

    class Meta:
        model = Branch
        fields = ["label", "value"]


class BranchSerializer(serializers.ModelSerializer):
    financial_institute = FinancialInstituteSerializer(many=False, read_only=True)

    class Meta:
        model = Branch
        fields = ["fi_branch_id", "branch_nm", "fi_id", "financial_institute_type", "geo_area"]


class DepartmentSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name', read_only=True)
    value = serializers.CharField(source='id', read_only=True)

    class Meta:
        model = Department
        fields = ["label", "value"]
