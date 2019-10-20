import datetime

from allauth.account.models import EmailAddress
from django.db import transaction
from rest_auth.views import PasswordResetConfirmView, sensitive_post_parameters_m
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    renderer_classes = [TemplateHTMLRenderer]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(template_name='password/password_reset_done.html')


class UserDeactivateView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        timestamp = int(datetime.datetime.now().timestamp() * 10 ** 6)
        deactivating_user = request.user
        with transaction.atomic():
            deactivating_user.is_active = False
            deactivating_user.username = f'탈퇴{timestamp}'
            deactivating_user.full_name = '(탈퇴 사용자)'
            deactivating_user.email = f'deactivated_{timestamp}'
            EmailAddress.objects.get(user=deactivating_user).delete()
            deactivating_user.job_histories.update(confirmation_information='')
            deactivating_user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
