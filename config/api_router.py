from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from ereturns.institutes.api.views import FinancialInstituteViewSet
from ereturns.rit.api.views import (
    RitDownloadViewSet, RitFeaturesViewSet, RitSupervisionViewSet,
    RitFrequencyViewSet, RitReportViewSet, RitUploadStatusViewSet,
    RitValidationViewSet
)
from ereturns.users.api.views import UserViewSet, UserRegistrationViewSet, UserPasswordChangeViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("users/me", UserPasswordChangeViewSet)
router.register("registration", UserRegistrationViewSet)


router.register("rit", RitFrequencyViewSet)
router.register("rit", RitFeaturesViewSet)
router.register("rit/supervision", RitUploadStatusViewSet)
router.register("rit", RitSupervisionViewSet)
router.register("rit", RitDownloadViewSet)
router.register("rit/report", RitReportViewSet)
router.register("rit", RitValidationViewSet)

router.register("institutes", FinancialInstituteViewSet)


app_name = "api"
urlpatterns = router.urls
