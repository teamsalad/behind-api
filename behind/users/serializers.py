from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from users.models import ROLES
from companies.serializers import UserJobHistorySerializer

UserModel = get_user_model()


class UserRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(
        required=True,
        choices=ROLES
    )

    def update(self, instance, validated_data):
        return super(RegisterSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        return super(RegisterSerializer, self).create(validated_data)


class UserDetailsSerializer(serializers.ModelSerializer):
    job_histories = UserJobHistorySerializer(many=True)

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'username',
                  'role', 'introduction', 'job_histories',)
        read_only_fields = ('id', 'email', 'job_histories',)
