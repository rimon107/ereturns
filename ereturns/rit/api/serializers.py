from django.contrib.auth import get_user_model
from rest_framework import serializers

from ereturns.rit.constants import RitFrequency, RitStatus, RitSupervisionStatus, FileType
from ereturns.rit.models.models import RitFeatures, RitSupervision, RitManagement, RitCoaValidation, RitCurrencyValidation
from ereturns.common.library import ChoiceField

User = get_user_model()


class BaseRitFeaturesSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='name', read_only=True)
    value = serializers.CharField(source='code', read_only=True)

    class Meta:
        model = RitFeatures
        fields = ["label", "value"]


class RitFeaturesSerializer(serializers.ModelSerializer):
    frequency = ChoiceField(choices=RitFrequency.Frequency)
    status = ChoiceField(choices=RitStatus.Status)
    # department = DepartmentSerializer(many=False, read_only=True)
    department = serializers.SerializerMethodField()
    # department_name = serializers.RelatedField(source='department.name', read_only=True)

    class Meta:
        model = RitFeatures
        fields = ["id", "code", "name", "frequency", "version", "department",
                  "column", "row", "cut_off_days", "status", "validate"]


class RitFeaturesSerializer(serializers.ModelSerializer):
    frequency = ChoiceField(choices=RitFrequency.Frequency)
    status = ChoiceField(choices=RitStatus.Status)
    # department = DepartmentSerializer(many=False, read_only=True)
    department = serializers.SerializerMethodField()
    # department_name = serializers.RelatedField(source='department.name', read_only=True)

    class Meta:
        model = RitFeatures
        fields = ["id", "code", "name", "frequency", "version", "department",
                  "column", "row", "cut_off_days", "status", "validate"]

    def get_department(self, obj):
        return f"{obj.department.name}"


class RitSupervisionReadSerializer(serializers.ModelSerializer):
    rit = serializers.SerializerMethodField()
    financial_institute_type = serializers.SerializerMethodField()
    financial_institute = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    uploaded_by = serializers.SerializerMethodField()
    status = ChoiceField(choices=RitSupervisionStatus.Status)

    class Meta:
        model = RitSupervision
        fields = ["rit", "financial_institute_type", "financial_institute", "branch",
                  "department", "uploaded_by", "file", "base_date", "phone", "prepared_by",
                  "upload_time", "ip", "status" ]

    def get_rit(self, obj):
        return f"{obj.rit.name}"

    def get_financial_institute_type(self, obj):
        return f"{obj.financial_institute_type.name}({obj.financial_institute_type.code})"

    def get_financial_institute(self, obj):
        return f"{obj.financial_institute.name}({obj.financial_institute.code})"

    def get_branch(self, obj):
        return f"{obj.branch.name}({obj.branch.code})"

    def get_department(self, obj):
        return f"{obj.department.name}({obj.department.code})"

    def get_uploaded_by(self, obj):
        return f"{obj.uploaded_by.name}"


class RitSupervisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RitSupervision
        fields = ["rit", "financial_institute_type", "financial_institute", "branch",
                  "department", "uploaded_by", "file", "base_date", "phone", "prepared_by",
                  "upload_time", "ip", "status" ]


class RitManagementSerializer(serializers.ModelSerializer):
    file_type = ChoiceField(choices=FileType.Types)
    rit = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    uploaded_by = serializers.SerializerMethodField()

    class Meta:
        model = RitManagement
        fields = ["file_type", "rit", "department", "file",
                  "uploaded_by", "upload_time", "version"]

    def get_rit(self, obj):
        if obj.rit:
            return f"{obj.rit.name}"

    def get_department(self, obj):
        if obj.department:
            return f"{obj.department.name}"

    def get_uploaded_by(self, obj):
        return f"{obj.uploaded_by.name}"


class RitNonReportingBranchSerializer(serializers.ModelSerializer):
    financial_institute = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    branch_code = serializers.SerializerMethodField()
    user_code = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ["financial_institute", "branch_name", "branch_code",
                  "user_code", "user_name", "designation", "phone"]

    def get_financial_institute(self, obj):
        return f"{obj.financial_institute.name}"

    def get_branch_name(self, obj):
        return f"{obj.branch.name}"

    def get_branch_code(self, obj):
        return f"{obj.branch.code}"

    def get_user_code(self, obj):
        return f"{obj.username}"

    def get_user_name(self, obj):
        return f"{obj.name}"


# class RitCurrencyValidationSerializer(serializers.ModelSerializer):
#     rit = serializers.SerializerMethodField()
#
#     class Meta:
#         model = RitCurrencyValidation
#         fields = ["rit", "currency"]
#
#     def get_rit(self, obj):
#         if obj.rit:
#             return f"{obj.rit.name}"
#
#
# class RitCoaValidationSerializer(serializers.ModelSerializer):
#     rit = serializers.SerializerMethodField()
#
#     class Meta:
#         model = RitCoaValidation
#         fields = ["rit", "coa"]
#
#     def get_rit(self, obj):
#         if obj.rit:
#             return f"{obj.rit.name}"
