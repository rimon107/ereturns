from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from ereturns.institutes.models import Branch, FinancialInstitute,\
    FinancialInstituteType
from ereturns.users.constants import Status


class User(AbstractUser):
    """User model for ereturns."""

    username_validator = UnicodeUsernameValidator()

    name = models.CharField(_("name"), blank=True, max_length=255)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    user_code = models.CharField(_('user code'), max_length=255, blank=True)
    password = models.CharField(_('password'), max_length=128)
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
    department = models.CharField(_("department"), blank=True, null=True, max_length=255)
    status = models.IntegerField(choices=Status.Status, default=Status.OFFLINE)
    email = models.EmailField(_('email address'), blank=True)
    approved_time = models.DateTimeField(_('approved time'), blank=True, null=True)
    approved_by = models.ForeignKey(
        "self",
        related_name='user_approved_by',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    password_reset_time = models.DateTimeField(_('password reset time'), blank=True, null=True)
    last_password_update_time = models.DateTimeField(_('last password update time'), blank=True, null=True)
    first_approved_by = models.ForeignKey(
        "self",
        related_name='user_first_approved_by',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    second_approved_by = models.ForeignKey(
        "self",
        related_name='user_second_approved_by',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    change_approved_by = models.ForeignKey(
        "self",
        related_name='user_change_approved_by',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    designation = models.CharField(_("designation"), blank=True, max_length=255)
    mobile = models.CharField(_("mobile"), blank=True, max_length=255)
    phone = models.CharField(_("phone"), blank=True, max_length=255)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    password_updated_by = models.ForeignKey(
        "self",
        related_name='user_password_updated_by',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    random_string = models.CharField(_("random string"), blank=True, max_length=255)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
