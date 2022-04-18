from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.settings import api_settings

from ereturns.institutes.api.serializers import DepartmentSerializer
from ereturns.institutes.models import Department, Branch, GeoArea, FinancialInstitute
from ereturns.rit.api.manage_rit import ManageRit
from ereturns.rit.api.serializers import (
    RitFeaturesSerializer,
    RitSupervisionSerializer,
    RitSupervisionReadSerializer,
    BaseRitFeaturesSerializer,
    RitManagementSerializer,
    RitNonReportingBranchSerializer,
)
from ereturns.rit.constants import RitFrequency, FileType, RitStatus
from ereturns.rit.models.models import (
    RitFeatures,
    RitSupervision,
    RitManagement,
    RitCurrencyValidation,
    RitCoaValidation, RitRefCodeValidation, RitEcoSectorValidation, RitEcoPurposeValidation,
    RitSecurityCodeValidation, RitCountryValidation, RitProductTypeValidation,
    RitInstrumentTypeValidation, RitInvestorValidation, RitInvestorChannelValidation, RitCompanyValidation,
    RitEnterpriseTypeValidation, RitSectorMajorActivitiesValidation, RitProductCodeValidation,
    RitPayrecPurposeValidation, RitUnitOfMeasureValidation, RitRepTypeValidation, RitScheduledCodeValidation,
    RitTypeCodeValidation, RitCommodityValidation, RitLegalFormOfEnterpriseValidation, RitEnterpriseLocationValidation,
    RitFellowEnterpriseLocationValidation, RitCommonParentLocationValidation, RitInstrumentClassificationValidation,
    RitCreditorTypeValidation, RitSmeSubCategoryValidation, RitSmeCategoryValidation, RitLoanSegregationValidation,
    RitAccountNumberValidation, RitLoanClassIdValidation, RitCollateralIdValidation, RitIndustryScaleIdValidation,
    RitGenderCodeValidation, RitBankingClassValidation, RitDebitCardIndicatorCodeValidation,
    RitFrequencyIndicatorCodeValidation, RitAccountTypeCodeValidation, RitAgingRangeValidation,
    RitReportingAreaValidation, RitCaseTypeCodeValidation, RitLawSuitTypeCodeValidation, RitPerspectiveCodeValidation,
    RitLoanStatusValidation, RitTransactionTypeValidation
)


class RitFrequencyViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = BaseRitFeaturesSerializer
    queryset = RitFeatures.objects.all()

    @action(detail=False, methods=["GET"])
    def frequency(self, request):
        frequencies = []
        for key, value in RitFrequency.Frequency:
            freq_dict = dict()
            freq_dict["label"] = value
            freq_dict["value"] = key
            frequencies.append(freq_dict)
        return Response(data=frequencies)


class RitFeaturesViewSet(GenericViewSet):
    serializer_class = RitManagementSerializer
    queryset = RitFeatures.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"])
    def features(self, request):
        frequency_id = self.request.GET.get('frequency_id')
        if frequency_id:
            features = RitFeatures.objects.filter(frequency=frequency_id, status=RitStatus.ACTIVE).values().order_by("code")
            serializer = BaseRitFeaturesSerializer(features, many=True)
        else:
            features = RitFeatures.objects.select_related("department").order_by("code")
            serializer = RitFeaturesSerializer(features, many=True)
        return Response(serializer.data)


class RitUploadStatusViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RitSupervisionReadSerializer
    queryset = RitSupervision.objects.all()
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(uploaded_by=request.user).order_by("-upload_time")
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RitSupervisionViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RitSupervisionSerializer
    queryset = RitSupervision.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["POST"])
    def upload(self, request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        rit_file = request.data.get("file")
        rit_name = rit_file.name
        meta = {
            "rit": rit_name,
            "fi": request.data.get("financial_institute"),
            "branch": request.data.get("branch")
        }
        # req_data = request.data.copy()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_rit = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        uploaded_rit.ip = ip
        uploaded_rit.save()
        rit = ManageRit()
        rit.insert_into_db(uploaded_rit, meta)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class RitDownloadViewSet(GenericViewSet):
    serializer_class = RitManagementSerializer
    queryset = RitManagement.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"])
    def departments(self, request):
        departments = Department.objects.values("name", "id").order_by("name")
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def files(self, request):
        department_id = self.request.GET.get('department_id')
        rit_id = self.request.GET.get('rit_id')
        if department_id:
            files = self.queryset.filter(department_id=department_id, file_type=FileType.RIT)
            serializer = RitManagementSerializer(files, many=True, context={"request": request})
        elif rit_id:
            try:
                queryset = RitFeatures.objects.get(code=rit_id)
            except RitFeatures.DoesNotExist:
                data = {
                    "not_found": ["RIT not found"]
                }
                return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            serializer = RitFeaturesSerializer(queryset)
        else:
            files = self.queryset.filter(file_type__in=[FileType.REFERENCE,
                                                        FileType.USER_MANUAL,
                                                        FileType.USER_REGISTRATION_FORM]
                                         ).order_by("file_type")
            serializer = RitManagementSerializer(files, many=True, context={"request": request})
        return Response(serializer.data)


class RitReportViewSet(GenericViewSet):
    serializer_class = RitSupervisionSerializer
    queryset = RitSupervision.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"], url_path="upload-status/base-date-wise")
    def upload_status_base_date_wise(self, request):
        rit_id = self.request.GET.get('rit_id')
        fi_id = self.request.GET.get('fi_id')
        base_date = self.request.GET.get('base_date')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if rit_id and fi_id and base_date:
            query = {
                "rit_id": rit_id,
                "financial_institute_id": fi_id,
                "base_date__date": base_date
            }

            if date_from:
                query["upload_time__date__gte"] = date_from

            if date_to:
                query["upload_time__date__lte"] = date_to

            result = self.queryset.filter(**query).select_related("rit", "financial_institute_type",
                                                                  "financial_institute", "branch",
                                                                  "uploaded_by").order_by("rit_id")
            serializer = RitSupervisionSerializer(result, many=True, context={"request": request})
            return Response(serializer.data)
        else:
            data = {}
            if not fi_id:
                data["fi_name"] = [
                        "This field is required."
                    ]
            if not rit_id:
                data["rit_name"] = [
                        "This field is required."
                    ]
            if not base_date:
                data["base_date"] = [
                        "This field is required."
                    ]
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

    @action(detail=False, methods=["GET"], url_path="upload-status/bank-wise")
    def upload_status_bank_wise(self, request):
        rit_id = self.request.GET.get('rit_id')
        fi_id = self.request.GET.get('fi_id')
        date_from = self.request.GET.get('date_from')

        if rit_id and fi_id and date_from:
            query = {
                "rit_id": rit_id,
                "financial_institute_id": fi_id,
                "upload_time__date__gte": date_from
            }

            result = self.queryset.filter(**query).select_related("rit", "financial_institute_type",
                                                                  "financial_institute", "branch",
                                                                  "uploaded_by").order_by("rit_id")
            serializer = RitSupervisionSerializer(result, many=True, context={"request": request})
            return Response(serializer.data)
        else:
            data = {}
            if not fi_id:
                data["fi_name"] = [
                    "This field is required."
                ]
            if not rit_id:
                data["rit_name"] = [
                    "This field is required."
                ]
            if not date_from:
                data["date_from"] = [
                    "This field is required."
                ]
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

    @action(detail=False, methods=["GET"], url_path="upload-status/non-reporting-branch")
    def upload_status_non_reporting_branch(self, request):
        rit_id = self.request.GET.get('rit_id')
        fi_id = self.request.GET.get('fi_id')
        base_date = self.request.GET.get('base_date')

        if rit_id and fi_id and base_date:
            query = {
                "rit_id": rit_id,
                "financial_institute_id": fi_id,
                "base_date__date": base_date
            }

            reporting_branches = Q(id__in=self.queryset.filter(**query).values_list("branch__id", flat=True))
            fi_branches = Branch.objects.filter(financial_institute_id=fi_id)
            non_reporting_branches = fi_branches.filter(~reporting_branches).values_list("id", flat=True)
            User = get_user_model()
            users = User.objects.filter(branch__id__in=non_reporting_branches)
            serializer = RitNonReportingBranchSerializer(users, many=True)
            return Response(serializer.data)
        else:
            data = {}
            if not fi_id:
                data["fi_name"] = [
                    "This field is required."
                ]
            if not rit_id:
                data["rit_name"] = [
                    "This field is required."
                ]
            if not base_date:
                data["base_date"] = [
                    "This field is required."
                ]
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)


class RitValidationViewSet(GenericViewSet):
    queryset = RitFeatures.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=["GET"])
    def validation(self, request):
        code = self.request.GET.get('code')
        if code:
            fi_id = self.request.user.financial_institute_id
            fis = FinancialInstitute.objects.values_list("fi_id", flat=True)
            branches = Branch.objects.filter(fi_id=fi_id).values_list("fi_branch_id", flat=True)
            district = GeoArea.objects.values_list("district", flat=True).distinct()
            currency = RitCurrencyValidation.objects.filter(rit__code=code).values_list("currency", flat=True)
            coa = RitCoaValidation.objects.filter(rit__code=code).values_list("coa", flat=True)
            refs = RitRefCodeValidation.objects.filter(rit__code=code).values("type", "code")
            eco_sector = RitEcoSectorValidation.objects.filter(rit__code=code).values_list("sector", flat=True)
            eco_purpose = RitEcoPurposeValidation.objects.filter(rit__code=code).values_list("purpose", flat=True)
            country = RitCountryValidation.objects.filter(rit__code=code).values_list("country", flat=True)
            product_type = RitProductTypeValidation.objects.filter(rit__code=code).values_list("product_type",
                                                                                               flat=True)
            product_code = RitProductCodeValidation.objects.filter(rit__code=code).values_list("product_code",
                                                                                               flat=True)
            instrument_type = RitInstrumentTypeValidation.objects.filter(rit__code=code).values_list("instrument_type",
                                                                                                     flat=True)
            investor = RitInvestorValidation.objects.filter(rit__code=code).values_list("investor", flat=True)
            security_code = RitSecurityCodeValidation.objects.filter(rit__code=code).values_list("security_code",
                                                                                                 flat=True)
            investor_channel = RitInvestorChannelValidation.objects.filter(rit__code=code).\
                values_list("investor_channel", flat=True)
            company = RitCompanyValidation.objects.filter(rit__code=code).values_list("company", flat=True)
            enterprise_type = RitEnterpriseTypeValidation.objects.filter(rit__code=code).\
                values_list("enterprise_type", flat=True)
            sector_major_activities = RitSectorMajorActivitiesValidation.objects.filter(rit__code=code). \
                values_list("sector_major_activities", flat=True)
            payrec_purpose = RitPayrecPurposeValidation.objects.filter(rit__code=code).\
                values_list("payrec_purpose", flat=True)
            unit_of_measure = RitUnitOfMeasureValidation.objects.filter(rit__code=code). \
                values_list("unit_of_measure", flat=True)
            rep_type = RitRepTypeValidation.objects.filter(rit__code=code).values_list("rep_type", flat=True)
            scheduled_code = RitScheduledCodeValidation.objects.filter(rit__code=code).\
                values_list("scheduled_code", flat=True)
            type_code = RitTypeCodeValidation.objects.filter(rit__code=code).values_list("type_code", flat=True)
            commodity = RitCommodityValidation.objects.filter(rit__code=code).values_list("commodity", flat=True)
            legal_form_of_enterprise = RitLegalFormOfEnterpriseValidation.objects.filter(rit__code=code).\
                values_list("legal_form_of_enterprise", flat=True)
            enterprise_location = RitEnterpriseLocationValidation.objects.filter(rit__code=code). \
                values_list("enterprise_location", flat=True)
            fellow_enterprise_location = RitFellowEnterpriseLocationValidation.objects.filter(rit__code=code). \
                values_list("fellow_enterprise_location", flat=True)
            common_parent_location = RitCommonParentLocationValidation.objects.filter(rit__code=code). \
                values_list("common_parent_location", flat=True)
            instrument_classification = RitInstrumentClassificationValidation.objects.filter(rit__code=code). \
                values_list("instrument_classification", flat=True)
            creditor_type = RitCreditorTypeValidation.objects.filter(rit__code=code).\
                values_list("creditor_type", flat=True)
            sme_category = RitSmeCategoryValidation.objects.filter(rit__code=code). \
                values_list("sme_category", flat=True)
            sme_sub_category = RitSmeSubCategoryValidation.objects.filter(rit__code=code). \
                values_list("sme_sub_category", flat=True)
            loan_segregation = RitLoanSegregationValidation.objects.filter(rit__code=code). \
                values_list("loan_segregation", flat=True)
            account_number = RitAccountNumberValidation.objects.filter(rit__code=code). \
                values_list("account_number", flat=True)
            gender_code = RitGenderCodeValidation.objects.filter(rit__code=code). \
                values_list("gender_code", flat=True)
            industry_scale_id = RitIndustryScaleIdValidation.objects.filter(rit__code=code). \
                values_list("industry_scale_id", flat=True)
            collateral_id = RitCollateralIdValidation.objects.filter(rit__code=code). \
                values_list("collateral_id", flat=True)
            loan_class_id = RitLoanClassIdValidation.objects.filter(rit__code=code). \
                values_list("loan_class_id", flat=True)
            freq_ind_code = RitFrequencyIndicatorCodeValidation.objects.filter(rit__code=code). \
                values_list("freq_ind_code", flat=True)
            debit_card_ind_code = RitDebitCardIndicatorCodeValidation.objects.filter(rit__code=code). \
                values_list("debit_card_ind_code", flat=True)
            banking_class = RitBankingClassValidation.objects.filter(rit__code=code). \
                values_list("banking_class", flat=True)
            aging_range_id = RitAgingRangeValidation.objects.filter(rit__code=code). \
                values_list("aging_range_id", flat=True)
            account_type_code = RitAccountTypeCodeValidation.objects.filter(rit__code=code). \
                values_list("account_type_code", flat=True)
            reporting_area = RitReportingAreaValidation.objects.filter(rit__code=code). \
                values_list("reporting_area", flat=True)
            lawsuit_type_code = RitLawSuitTypeCodeValidation.objects.filter(rit__code=code). \
                values_list("lawsuit_type_code", flat=True)
            case_type_code = RitCaseTypeCodeValidation.objects.filter(rit__code=code). \
                values_list("case_type_code", flat=True)
            perspective_code = RitPerspectiveCodeValidation.objects.filter(rit__code=code). \
                values_list("perspective_code", flat=True)
            transaction_type = RitTransactionTypeValidation.objects.filter(rit__code=code). \
                values_list("transaction_type", flat=True)
            loan_status = RitLoanStatusValidation.objects.filter(rit__code=code). \
                values_list("loan_status", flat=True)

            data = {
                "fis": fis,
                "branches": branches,
                "district": district,
                "currency": currency,
                "coa": coa,
                "eco_sector": eco_sector,
                "eco_purpose": eco_purpose,
                "country": country,
                "product_type": product_type,
                "product_code": product_code,
                "instrument_type": instrument_type,
                "investor": investor,
                "security_code": security_code,
                "investor_channel": investor_channel,
                "company": company,
                "enterprise_type": enterprise_type,
                "sector_major_activities": sector_major_activities,
                "payrec_purpose": payrec_purpose,
                "unit_of_measure": unit_of_measure,
                "rep_type": rep_type,
                "scheduled_code": scheduled_code,
                "type_code": type_code,
                "commodity": commodity,
                "legal_form_of_enterprise": legal_form_of_enterprise,
                "enterprise_location": enterprise_location,
                "fellow_enterprise_location": fellow_enterprise_location,
                "common_parent_location": common_parent_location,
                "instrument_classification": instrument_classification,
                "creditor_type": creditor_type,
                "sme_category": sme_category,
                "sme_sub_category": sme_sub_category,
                "loan_segregation": loan_segregation,
                "account_number": account_number,
                "gender_code": gender_code,
                "industry_scale_id": industry_scale_id,
                "collateral_id": collateral_id,
                "loan_class_id": loan_class_id,
                "freq_ind_code": freq_ind_code,
                "debit_card_ind_code": debit_card_ind_code,
                "banking_class": banking_class,
                "aging_range_id": aging_range_id,
                "account_type_code": account_type_code,
                "reporting_area": reporting_area,
                "lawsuit_type_code": lawsuit_type_code,
                "case_type_code": case_type_code,
                "perspective_code": perspective_code,
                "transaction_type": transaction_type,
                "loan_status": loan_status
            }

            if refs.exists():
                from collections import defaultdict
                ref_dict = defaultdict(list)
                for ref in refs:
                    ref_dict[ref["type"]].append(ref["code"])
                data.update(ref_dict)
            return Response(data)
        data = {
            "rit_code": ["RIT Code required"]
        }
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
