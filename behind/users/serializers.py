from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import PasswordResetSerializer

from users.models import ROLES
from companies.serializers import UserJobHistorySerializer

UserModel = get_user_model()


class UserRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(
        required=True,
        max_length=30
    )
    role = serializers.ChoiceField(
        required=True,
        choices=ROLES
    )

    def custom_signup(self, request, user):
        user.full_name = request.data['full_name']
        user.role = request.data['role']
        user.save()

    @transaction.atomic
    def update(self, instance, validated_data):
        return super(RegisterSerializer, self).update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        return super(RegisterSerializer, self).create(validated_data)


class UserDetailsSerializer(serializers.ModelSerializer):
    job_histories = UserJobHistorySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'username',
                  'role', 'full_name', 'job_seeker_intro',
                  'employee_intro', 'job_histories',)
        read_only_fields = ('id', 'email', 'job_histories',)


class UserPasswordResetSerializer(PasswordResetSerializer):
    @transaction.atomic
    def update(self, instance, validated_data):
        return super(PasswordResetSerializer, self).update(instance, validated_data)

    @transaction.atomic
    def create(self, validated_data):
        return super(PasswordResetSerializer, self).create(validated_data)

    def get_email_options(self):
        return {
            'subject_template_name': 'password/email/password_reset_subject.txt',
            'email_template_name': 'password/email/password_reset_email.html',
            'html_email_template_name': 'password/email/password_reset_email.html',
            'extra_email_context': {
                'absolute_uri': self.context['request'].build_absolute_uri()
            }
        }
