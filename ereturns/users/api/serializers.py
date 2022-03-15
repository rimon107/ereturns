from django.contrib.auth import get_user_model
from rest_framework import serializers
from ereturns.common.library import ChoiceField
from ereturns.institutes.models import Branch
from ereturns.users.constants import Status

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "user_code", "username", "name"]


class UserSerializer(serializers.ModelSerializer):
    financial_institute_type = serializers.SerializerMethodField()
    financial_institute = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    status = ChoiceField(choices=Status.Status)

    class Meta:
        model = User
        fields = ["id", "user_code", "username", "name", "financial_institute_type",
                  "financial_institute", "branch", "status", "email", "designation", "department",
                  "mobile", "phone", "last_login", "is_active", "is_active",
                  "change_approved_by", "approved_time", "approved_by", "password_reset_time",
                  "last_password_update_time", "first_approved_by", "second_approved_by",
                  "date_joined","password_updated_by", "random_string", "groups"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "id"}
        }

    def get_serializer_context(self):
        return self.context['request'].data

    def create(self, validated_data):
        request_data = dict(self.get_serializer_context())
        groups_data = validated_data.pop('groups')
        password = request_data.get("password")
        validated_data["financial_institute_type_id"] = request_data.get("financial_institute_type_id")
        validated_data["financial_institute_id"] = request_data.get("financial_institute_id")
        if request_data.get("branch_id"):
            branch = request_data.get("branch_id")
        else:
            fi_id = request_data.get("financial_institute_id")
            branch = Branch.objects.filter(fi_id=fi_id, branch_nm__iexact="Head Office")
            if branch.exists():
                branch = branch.first().fi_branch_id
            else:
                raise serializers.ValidationError({'branch_not_exists': ("The branch does not exists.")})
        validated_data["branch_id"] = branch

        instance = User.objects.create(**validated_data)
        instance.set_password(password)
        instance.save()
        for group_data in groups_data:
            instance.groups.add(group_data)
        return instance

    def get_financial_institute_type(self, obj):
        fi_type = {
            "id": obj.financial_institute_type.id if obj.financial_institute_type else None,
            "name": obj.financial_institute_type.name if obj.financial_institute_type else None,
        }
        return fi_type

    def get_financial_institute(self, obj):
        fi = {
            "id": obj.financial_institute.fi_id if obj.financial_institute else None,
            "name": obj.financial_institute.fi_nm if obj.financial_institute else None,
        }
        return fi

    def get_branch(self, obj):
        branch = {
            "id": obj.branch.fi_branch_id if obj.branch else None,
            "name": obj.branch.branch_nm if obj.branch else None,
        }
        return branch


class UserPasswordUpdateSerializer(serializers.Serializer):

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'current_password', 'new_password', 'confirm_password'
        ]
