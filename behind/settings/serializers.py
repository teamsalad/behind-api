from rest_framework import serializers

from settings.models import PushNotificationSetting


class PushNotificationSettingSerializer(serializers.ModelSerializer):
    chat = serializers.BooleanField()
    answered = serializers.BooleanField()
    asked = serializers.BooleanField()

    class Meta:
        model = PushNotificationSetting
        fields = ('id', 'chat', 'answered', 'asked',)
        read_only_fields = ('id',)
