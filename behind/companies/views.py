from django.core import signing
from django.http import Http404
from django.views.generic.base import TemplateResponseMixin, View
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from behind import settings
from companies.models import Company, Job, UserJobHistory
from .serializers import (
    UserJobHistorySerializer,
    CreateUserJobHistorySerializer,
    CompanySerializer,
    JobSerializer,
)


class UserJobHistoryConfirmView(TemplateResponseMixin, View):
    template_name = 'allauth/account/email_confirm.html'

    def get_object(self):
        try:
            key = self.kwargs['key']
            max_age = (60 * 60 * 24 *
                       settings.EMAIL_CONFIRMATION_EXPIRE_DAYS)
            company_email = signing.loads(
                key,
                max_age=max_age,
                salt=settings.SALT
            )
            return UserJobHistory.objects.get(
                confirmation_information=company_email)
        except (signing.SignatureExpired,
                signing.BadSignature,):
            ValidationError({
                'key': 'Signature expired, bad signature.'
            })
        except UserJobHistory.DoesNotExist:
            raise Http404()

    def get(self, *args, **kwargs):
        confirming_user_job_history = self.get_object()
        confirming_user_job_history.confirm()
        return self.render_to_response(kwargs)


class UserJobHistoryListView(ListAPIView):
    """
    List job histories,
    create new job history
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.job_histories.all()

    def get_serializer_context(self):
        context = (
            super(UserJobHistoryListView, self).get_serializer_context()
        )
        context.update({
            'current_user': self.request.user,
        })
        return context

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserJobHistorySerializer
        return UserJobHistorySerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CompanyListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class JobListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = JobSerializer
    queryset = Job.objects.all()
