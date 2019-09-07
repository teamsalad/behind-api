from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

UserModel = get_user_model()


class UserRegisterSerializer(RegisterSerializer):
    role = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        return super(RegisterSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        return super(RegisterSerializer, self).create(validated_data)


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'role',)
        read_only_fields = ('email',)
