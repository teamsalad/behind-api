from rest_framework import serializers

from settings.models import PushNotificationSetting, AppVersion


class PushNotificationSettingSerializer(serializers.ModelSerializer):
    chat = serializers.BooleanField()
    answered = serializers.BooleanField()
    asked = serializers.BooleanField()

    class Meta:
        model = PushNotificationSetting
        fields = ('id', 'chat', 'answered', 'asked',)
        read_only_fields = ('id',)


class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = (
            'id', 'name', 'code', 'device_type',
            'release_state', 'update_state', 'created_at',
        )
        read_only_fields = (
            'id', 'name', 'code', 'device_type',
            'release_state', 'update_state', 'created_at',
        )
