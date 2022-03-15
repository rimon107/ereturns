from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _


class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})

        refresh_token = self.request.data.get('refresh')
        try:
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            data = {
                "msg": "Logout successful."
            }
        except:
            data = {
                "msg": ('Already logged out')
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        return Response(status=status.HTTP_200_OK, data=data)
