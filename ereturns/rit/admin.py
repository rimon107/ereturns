from django.contrib import admin
from ereturns.rit.models.models import (
    RitFeatures,
    RitSupervision,
    RitManagement,
    RitCurrencyValidation,
    RitCoaValidation
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
    search_fields = ["rit"]
    autocomplete_fields = ('rit', )
