from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView

from settings.models import PushNotificationSetting
from settings.serializers import PushNotificationSettingSerializer


class PushNotificationSettingView(RetrieveUpdateAPIView):
    """
    Update or get push notification settings
    """
    serializer_class = PushNotificationSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return PushNotificationSetting.objects.get_or_create(user=self.request.user)[0]
