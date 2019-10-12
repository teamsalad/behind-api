from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView

from settings.models import PushNotificationSetting, AppVersion
from settings.serializers import PushNotificationSettingSerializer, AppVersionSerializer


class PushNotificationSettingView(RetrieveUpdateAPIView):
    """
    Update or get push notification settings
    """
    serializer_class = PushNotificationSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return PushNotificationSetting.objects.get_or_create(user=self.request.user)[0]


class AppVersionView(RetrieveAPIView):
    """
    Get latest app version
    """
    serializer_class = AppVersionSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        device_dict = {'ios': 1, 'android': 2, 'web': 3}
        try:
            device_type = device_dict[self.kwargs['device_type']]
            app_version = AppVersion.objects \
                .filter(device_type=device_type) \
                .order_by('-created_at').first()
            if app_version is None:
                raise Http404
            return app_version
        except KeyError:
            raise Http404
