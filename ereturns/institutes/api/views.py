from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from ereturns.institutes.api.serializers import (
    BaseFinancialInstituteSerializer, BaseBranchSerializer
)
from ereturns.institutes.models import FinancialInstitute, Branch
from django.db.models import Q

from ereturns.users.constants import GroupNames

User = get_user_model()


class FinancialInstituteViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny, )
    serializer_class = BaseFinancialInstituteSerializer
    queryset = FinancialInstitute.objects.all()
    lookup_field = "fi_id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(~Q(fi_nm__iexact="Bangladesh Bank")).order_by("fi_nm")

    @action(detail=False, methods=["GET"])
    def branch(self, request):
        fi_id = self.request.GET.get('fi_id')
        queryset = Branch.objects.filter(fi_id=fi_id).exclude(branch_nm__iexact="Head Office").order_by("branch_nm")
        serializer = BaseBranchSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="user-count")
    def user_count(self, request):
        fi_id = self.request.GET.get('fi_id')
        queryset = User.objects.filter(financial_institute__fi_id=fi_id)
        branch_id = self.request.GET.get('branch_id')
        ho_users = queryset.filter(groups__name=GroupNames.bank_ho_end_user).count()
        data = {
            "ho_users": ho_users
        }
        if branch_id:
            branch_users = queryset.filter(branch_id=branch_id, groups__name=GroupNames.bank_branch_end_user).count()
            data["branch_users"] = branch_users

        return Response(status=status.HTTP_200_OK, data=data)
