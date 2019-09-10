from rest_framework import serializers

from .models import Job, Company, UserJobHistory


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'title')
        read_only_fields = ('id', 'title',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'email_domain',)
        read_only_fields = ('id', 'name', 'email_domain',)


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
