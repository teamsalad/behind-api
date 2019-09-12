from allauth.utils import build_absolute_uri
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from behind import settings
from .models import Job, Company, UserJobHistory, METHODS
from rest_framework import serializers
from django.core import signing
from allauth.account.adapter import DefaultAccountAdapter


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'title',)
        read_only_fields = ('id', 'title',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'email_domain',)
        read_only_fields = ('id', 'name', 'email_domain',)


class CreateUserJobHistorySerializer(serializers.ModelSerializer):
    company_email = serializers.EmailField(
        write_only=True,
        required=True,
        allow_blank=False
    )
    confirmation_method = serializers.ChoiceField(
        choices=METHODS,
        default=METHODS[0][0]
    )
    job_id = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Job.objects.all(),
        write_only=True
    )
    company = CompanySerializer(read_only=True)
    job = JobSerializer(read_only=True)

    def create(self, validated_data):
        if validated_data.get('confirmation_method') == METHODS[0][0]:
            company_email = validated_data.pop('company_email')
            if UserJobHistory.objects.filter(confirmation_information=company_email).exists():
                raise serializers.ValidationError({
                    'company_email': 'Already exists.'
                })
            company_domain = company_email.split("@")[1]
            validated_data['job_id'] = validated_data['job_id'].id
            validated_data['user'] = self.context['current_user']
            validated_data['company'] = Company.objects.get(email_domain=company_domain)
            validated_data['confirmation_information'] = company_email
            self._send_confirmation_mail(self.context['request'], company_email)
        return UserJobHistory.objects.create(**validated_data)

    def _send_confirmation_mail(self, request, company_email):
        """
        XXX: This method is a modified version
        from allauth.account.adapter

        :param request:
        :param company_email:
        :return: None
        """
        adapter = DefaultAccountAdapter()
        current_site = get_current_site(request)
        key = signing.dumps(
            obj=company_email,
            salt=settings.SALT)
        url = reverse(
            "confirm_company_email",
            args=[key])
        activate_url = build_absolute_uri(
            request,
            url)
        ctx = {
            "user": request.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": key,
        }
        email_template = 'account/email/company_email_confirmation'
        adapter.send_mail(email_template,
                          company_email,
                          ctx)

    class Meta:
        model = UserJobHistory
        fields = (
            'id', 'company', 'job', 'job_id', 'confirmation_method',
            'confirmation_information', 'confirmed', 'created_at',
            'company_email',
        )
        read_only_fields = (
            'id', 'company', 'job',
            'confirmation_information', 'created_at',
            'confirmed', 'confirmation_method',
        )


class UserJobHistorySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = UserJobHistory
        fields = (
            'id', 'company', 'job', 'confirmation_method',
            'confirmation_information', 'confirmed', 'created_at'
        )
        read_only_fields = ('id', 'company', 'job', 'created_at')
