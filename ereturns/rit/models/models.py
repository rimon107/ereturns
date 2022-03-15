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
