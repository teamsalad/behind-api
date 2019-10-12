from django.db import models

from behind import settings

DEVICE_TYPES = (
    (1, 'ios'),
    (2, 'android'),
    (3, 'web'),
)
RELEASE_STATE = (
    (1, 'released'),
    (2, 'in_review'),
    (3, 'rejected'),
)
UPDATE_STATE = (
    (1, 'no_alert'),
    (2, 'alert'),
    (3, 'force_alert'),
)


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


class AppVersion(models.Model):
    name = models.CharField(max_length=20)
    code = models.PositiveIntegerField()
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPES)
    release_state = models.PositiveSmallIntegerField(
        choices=RELEASE_STATE,
        default=RELEASE_STATE[1][0]
    )
    update_state = models.PositiveSmallIntegerField(
        choices=UPDATE_STATE,
        default=UPDATE_STATE[0][0]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_versions"
