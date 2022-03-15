from django.db import models
from django.utils.translation import gettext_lazy as _


class GeoArea(models.Model):
    geo_area_id = models.IntegerField(_("Geo Area ID"), primary_key=True)
    country_id = models.IntegerField(_("Country ID"))
    division = models.CharField(_("Division"), max_length=255)
    district = models.CharField(_("District"), max_length=255)
    thana_upazilla = models.CharField(_("Upazila"), max_length=255)

    def __str__(self):
        return f"{self.division}-{self.district}-{self.thana_upazilla}"

    class Meta:
        db_table = 'd_geo_area'


class FinancialInstituteType(models.Model):
    code = models.CharField(_("code"), blank=True, max_length=255)
    name = models.CharField(_("financial institute type"), blank=True, max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'd_fi_type'


class FinancialInstitute(models.Model):
    fi_id = models.IntegerField(_("FI ID"), primary_key=True)
    fi_nm = models.CharField(_("financial institute"), max_length=255)
    fi_alias = models.CharField(_("alias"), max_length=255)
    geo_area = models.ForeignKey(
        GeoArea,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    fi_class_id = models.IntegerField(_("FI Class ID"))
    fi_status = models.IntegerField(_("FI Status"))
    financial_institute_type = models.ForeignKey(
        FinancialInstituteType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.fi_nm}"

    class Meta:
        db_table = 'd_fi'


class Branch(models.Model):
    fi_branch_id = models.IntegerField(_("FI Branch ID"), primary_key=True)
    fi_id = models.ForeignKey(
        FinancialInstitute,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    branch_nm = models.CharField(_("Branch Name"), max_length=255)
    geo_area = models.ForeignKey(
        GeoArea,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.branch_nm}({self.fi_branch_id})"

    class Meta:
        db_table = 'd_fi_branch'


class Department(models.Model):
    code = models.CharField(_("code"), blank=True, max_length=255)
    name = models.CharField(_("department"), blank=True, max_length=255)
    financial_institute_type = models.ForeignKey(
        FinancialInstituteType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    financial_institute = models.ForeignKey(
        FinancialInstitute,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.code}"

    class Meta:
        db_table = 'department'
