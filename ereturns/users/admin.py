from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ereturns.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Other info"),
            {
                "fields": (
                    "user_code",
                    "financial_institute_type",
                    "financial_institute",
                    "branch",
                    "department",
                    "status",
                    "designation",
                    "mobile",
                    "phone",
                    "approved_by",
                    "approved_time",
                    "password_reset_time",
                    "last_password_update_time",
                    "first_approved_by",
                    "second_approved_by",
                    "change_approved_by",
                    "password_updated_by",
                    "random_string"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    autocomplete_fields = ('financial_institute', 'branch',)
