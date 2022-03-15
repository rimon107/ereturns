from django.contrib import admin

from ereturns.institutes.models import (
    FinancialInstitute, Branch,
    FinancialInstituteType,
    GeoArea, Department
)


admin.site.register(FinancialInstituteType)


@admin.register(GeoArea)
class GeoAreaAdmin(admin.ModelAdmin):
    search_fields = ['thana_upazilla']


@admin.register(FinancialInstitute)
class FinancialInstituteAdmin(admin.ModelAdmin):
    list_display = ["fi_id", "fi_nm", "fi_alias"]
    search_fields = ["fi_nm"]
    autocomplete_fields = ('geo_area', )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["fi_id", "fi_branch_id", "branch_nm"]
    search_fields = ['fi_id__fi_nm', 'geo_area__geo_area_id']
    autocomplete_fields = ('fi_id', 'geo_area')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "financial_institute"]
    search_fields = ('financial_institute', 'branch')
    autocomplete_fields = ('financial_institute', 'branch')
