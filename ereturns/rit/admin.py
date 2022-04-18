from django.contrib import admin
from ereturns.rit.models.models import (
    RitFeatures,
    RitSupervision,
    RitManagement,
    RitCurrencyValidation,
    RitCoaValidation, RitLoadStatus
)


@admin.register(RitManagement)
class RitManagementAdmin(admin.ModelAdmin):
    fieldsets = (
        (("Rit Management"),
         {"fields": ("file_type",
                     "rit",
                     "department",
                     "file",
                     "uploaded_by",
                     "upload_time",
                     "version"
                     )}),
    )
    list_display = ["file_type", "rit", "file"]
    search_fields = ["rit"]
    autocomplete_fields = ('rit',)


@admin.register(RitFeatures)
class RitFeaturesAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(RitCurrencyValidation)
class RitCurrencyValidationAdmin(admin.ModelAdmin):
    search_fields = ["rit"]
    autocomplete_fields = ('rit', )


@admin.register(RitCoaValidation)
class RitCoaValidationAdmin(admin.ModelAdmin):
    search_fields = ["rit"]
    autocomplete_fields = ('rit', )


@admin.register(RitSupervision)
class RitSupervisionAdmin(admin.ModelAdmin):
    search_fields = ["rit", "financial_institute"]
    autocomplete_fields = ('rit',)
    list_display = ["rit", "financial_institute", "branch", "base_date", "upload_time"]


@admin.register(RitLoadStatus)
class RitLoadStatusAdmin(admin.ModelAdmin):
    search_fields = ["rit_name", "fi", "branch", "status", "msg", "count", "load_date"]
    list_display = ["rit_name", "fi", "branch", "status", "msg", "count", "load_date"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
