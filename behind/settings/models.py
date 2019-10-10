from django.db import models

from behind import settings


class PushNotificationSetting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='push_notification_setting'
    )
    chat = models.BooleanField(default=True)
    answered = models.BooleanField(default=True)
    asked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "push_notification_settings"
