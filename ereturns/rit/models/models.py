from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from ereturns.common.file_upload import directory_path, rit_directory_path
from ereturns.institutes.models import FinancialInstitute, Branch, Department, FinancialInstituteType
from ereturns.rit.constants import RitStatus, RitFrequency, RitSupervisionStatus, FileType

User = get_user_model()


class RitFeatures(models.Model):
    code = models.CharField(_("code"), blank=False, max_length=255)
    name = models.CharField(_("name"), blank=False, max_length=255)
    frequency = models.IntegerField(choices=RitFrequency.Frequency, default=RitFrequency.DAILY)
    version = models.FloatField(_("version"), blank=True)
    column = models.IntegerField(_("column(s)"))
    row = models.IntegerField(_("row(s)"))
    cut_off_days = models.IntegerField(_("cut off day(s)"))
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    status = models.IntegerField(choices=RitStatus.Status, default=RitStatus.INACTIVE)
    validate = models.BooleanField(
        _('validate'),
        default=False,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'rit_features'


class RitSupervision(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=False
    )
    financial_institute_type = models.ForeignKey(
        FinancialInstituteType,
        on_delete=models.CASCADE,
        blank=False
    )
    financial_institute = models.ForeignKey(
        FinancialInstitute,
        on_delete=models.CASCADE,
        blank=False
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        blank=False
    )
    department = models.CharField(_("department"), blank=True, null=True, max_length=255)
    base_date = models.DateTimeField(_('base date'), blank=False)
    file = models.FileField(upload_to=directory_path, blank=False)
    phone = models.CharField(_("phone"), blank=True, max_length=255)
    prepared_by = models.CharField(_("prepared by"), blank=True, null=True, max_length=255)
    uploaded_by = models.ForeignKey(
        User,
        related_name='user_uploaded_by',
        on_delete=models.CASCADE,
        blank=False
    )
    upload_time = models.DateTimeField(_('upload time'), default=timezone.now)
    status = models.IntegerField(choices=RitSupervisionStatus.Status, default=RitSupervisionStatus.UPLOADED)
    ip = models.CharField(_("ip address"), blank=True, max_length=255)

    def __str__(self):
        return f"{self.rit.name}"

    class Meta:
        db_table = 'rit_supervision'


class RitManagement(models.Model):
    file_type = models.IntegerField(choices=FileType.Types, default=FileType.RIT)
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    file = models.FileField(upload_to=rit_directory_path, blank=False)
    uploaded_by = models.ForeignKey(
        User,
        related_name='rit_mgt_uploaded_by',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    upload_time = models.DateTimeField(_('upload time'), blank=False, default=timezone.now)
    version = models.CharField(_("version"), blank=True, null=True, max_length=255)

    def __str__(self):
        return f"{self.file.name}"

    class Meta:
        db_table = 'rit_management'


class RitLoadStatus(models.Model):
    rit_name = models.CharField(max_length=255, blank=True, null=True)
    fi = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    msg = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True, default=0)
    load_date = models.DateTimeField(_('Date'), default=timezone.now)

    def __str__(self):
        return f"{self.rit_name}-{self.load_date}"

    class Meta:
        db_table = 'rit_load_status'


class RitCurrencyValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    currency = models.IntegerField(_("Currency"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.currency}"

    class Meta:
        db_table = 'rit_validation_currency'


class RitCoaValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    coa = models.IntegerField(_("Chart of Account"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.coa}"

    class Meta:
        db_table = 'rit_validation_coa'


class RitRefCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    type = models.CharField(_("type"), blank=True, null=True, max_length=255)
    code = models.IntegerField(_("Ref Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.code}"

    class Meta:
        db_table = 'rit_validation_ref_code'


class RitEcoSectorValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    sector = models.IntegerField(_("Eco Sector"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.sector}"

    class Meta:
        db_table = 'rit_validation_eco_sector'


class RitEcoPurposeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    purpose = models.IntegerField(_("Eco Purpose"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.purpose}"

    class Meta:
        db_table = 'rit_validation_eco_purpose'


class RitCountryValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    country = models.IntegerField(_("Country ID"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.country}"

    class Meta:
        db_table = 'rit_validation_country'


class RitProductCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    product_code = models.IntegerField(_("Product Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.product_code}"

    class Meta:
        db_table = 'rit_validation_product_code'


class RitProductTypeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    product_type = models.IntegerField(_("Product Type"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.product_type}"

    class Meta:
        db_table = 'rit_validation_product_type'


class RitInstrumentTypeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    instrument_type = models.IntegerField(_("Instrument Type"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.instrument_type}"

    class Meta:
        db_table = 'rit_validation_instrument_type'


class RitInvestorValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    investor = models.IntegerField(_("Investor ID"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.investor}"

    class Meta:
        db_table = 'rit_validation_investor'


class RitSecurityCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    security_code = models.IntegerField(_("Investor ID"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.security_code}"

    class Meta:
        db_table = 'rit_validation_security_code'


class RitInvestorChannelValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    investor_channel = models.IntegerField(_("Investor Channel"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.investor_channel}"

    class Meta:
        db_table = 'rit_validation_investor_channel'


class RitCompanyValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    company = models.IntegerField(_("Company"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.company}"

    class Meta:
        db_table = 'rit_validation_company'


class RitEnterpriseTypeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    enterprise_type = models.IntegerField(_("Enterprise Type"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.enterprise_type}"

    class Meta:
        db_table = 'rit_validation_enterprise_type'


class RitSectorMajorActivitiesValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    sector_major_activities = models.IntegerField(_("Sector Major Activities"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.sector_major_activities}"

    class Meta:
        db_table = 'rit_validation_sector_major_activities'


class RitPayrecPurposeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    payrec_purpose = models.IntegerField(_("Pay Rec Purpose"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.payrec_purpose}"

    class Meta:
        db_table = 'rit_validation_payrec_purpose'


class RitUnitOfMeasureValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    unit_of_measure = models.IntegerField(_("Unit of Measure"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.unit_of_measure}"

    class Meta:
        db_table = 'rit_validation_unit_of_measure'


class RitRepTypeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    rep_type = models.IntegerField(_("Report Type"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.rep_type}"

    class Meta:
        db_table = 'rit_validation_rep_type'


class RitScheduledCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    scheduled_code = models.IntegerField(_("Scheduled Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.scheduled_code}"

    class Meta:
        db_table = 'rit_validation_scheduled_code'


class RitTypeCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    type_code = models.IntegerField(_("Type Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.type_code}"

    class Meta:
        db_table = 'rit_validation_type_code'


class RitCommodityValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    commodity = models.IntegerField(_("Commodity"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.commodity}"

    class Meta:
        db_table = 'rit_validation_commodity'


class RitLegalFormOfEnterpriseValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    legal_form_of_enterprise = models.IntegerField(_("Legal Form Of Enterprise"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.legal_form_of_enterprise}"

    class Meta:
        db_table = 'rit_validation_legal_form_of_enterprise'


class RitEnterpriseLocationValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    enterprise_location = models.IntegerField(_("Enterprise Location"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.enterprise_location}"

    class Meta:
        db_table = 'rit_validation_enterprise_location'


class RitFellowEnterpriseLocationValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    fellow_enterprise_location = models.IntegerField(_("Fellow Enterprise Location"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.fellow_enterprise_location}"

    class Meta:
        db_table = 'rit_validation_fellow_enterprise_location'


class RitCommonParentLocationValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    common_parent_location = models.IntegerField(_("Common Parent Location"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.common_parent_location}"

    class Meta:
        db_table = 'rit_validation_common_parent_location'


class RitInstrumentClassificationValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    instrument_classification = models.IntegerField(_("Instrument Classification"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.instrument_classification}"

    class Meta:
        db_table = 'rit_validation_instrument_classification'


class RitCreditorTypeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    creditor_type = models.IntegerField(_("Creditor Type"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.creditor_type}"

    class Meta:
        db_table = 'rit_validation_creditor_type'


class RitSmeCategoryValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    sme_category = models.IntegerField(_("SME Category"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.sme_category}"

    class Meta:
        db_table = 'rit_validation_sme_category'


class RitSmeSubCategoryValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    sme_sub_category = models.IntegerField(_("SME Sub Category"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.sme_sub_category}"

    class Meta:
        db_table = 'rit_validation_sme_sub_category'


class RitLoanSegregationValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    loan_segregation = models.IntegerField(_("Loan Segregation"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.loan_segregation}"

    class Meta:
        db_table = 'rit_validation_loan_segregation'


class RitAccountNumberValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    account_number = models.IntegerField(_("Account Number"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.account_number}"

    class Meta:
        db_table = 'rit_validation_account_number'


class RitGenderCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    gender_code = models.IntegerField(_("Gender Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.gender_code}"

    class Meta:
        db_table = 'rit_validation_gender_code'


class RitIndustryScaleIdValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    industry_scale_id = models.IntegerField(_("Industry Scale Id"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.industry_scale_id}"

    class Meta:
        db_table = 'rit_validation_industry_scale_id'


class RitCollateralIdValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    collateral_id = models.IntegerField(_("Collateral Id"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.collateral_id}"

    class Meta:
        db_table = 'rit_validation_collateral_id'


class RitLoanClassIdValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    loan_class_id = models.IntegerField(_("Loan Class Id"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.loan_class_id}"

    class Meta:
        db_table = 'rit_validation_loan_class_id'


class RitFrequencyIndicatorCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    freq_ind_code = models.IntegerField(_("Frequency Indicator Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.freq_ind_code}"

    class Meta:
        db_table = 'rit_validation_frequency_indicator_code'


class RitDebitCardIndicatorCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    debit_card_ind_code = models.IntegerField(_("Debit Card Indicator Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.debit_card_ind_code}"

    class Meta:
        db_table = 'rit_validation_debit_card_indicator_code'


class RitBankingClassValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    banking_class = models.IntegerField(_("Banking Class"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.banking_class}"

    class Meta:
        db_table = 'rit_validation_banking_class'


class RitAgingRangeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    aging_range_id = models.IntegerField(_("Aging Range"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.aging_range_id}"

    class Meta:
        db_table = 'rit_validation_aging_range_id'


class RitAccountTypeCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    account_type_code = models.IntegerField(_("Account Type"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.account_type_code}"

    class Meta:
        db_table = 'rit_validation_account_type_code'


class RitReportingAreaValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    reporting_area = models.IntegerField(_("Reporting Area"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.reporting_area}"

    class Meta:
        db_table = 'rit_validation_reporting_area'


class RitLawSuitTypeCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    lawsuit_type_code = models.IntegerField(_("Law Suit Type Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.lawsuit_type_code}"

    class Meta:
        db_table = 'rit_validation_lawsuit_type_code'


class RitCaseTypeCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    case_type_code = models.IntegerField(_("Case Type Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.case_type_code}"

    class Meta:
        db_table = 'rit_validation_case_type_code'


class RitPerspectiveCodeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    perspective_code = models.IntegerField(_("Perspective Code"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.perspective_code}"

    class Meta:
        db_table = 'rit_validation_perspective_code'


class RitTransactionTypeValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    transaction_type = models.IntegerField(_("Transaction Type"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.transaction_type}"

    class Meta:
        db_table = 'rit_validation_transaction_type'


class RitLoanStatusValidation(models.Model):
    rit = models.ForeignKey(
        RitFeatures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    loan_status = models.IntegerField(_("Loan Status"), blank=True, null=True)

    def __str__(self):
        return f"{self.rit.name}-{self.loan_status}"

    class Meta:
        db_table = 'rit_validation_loan_status'
