from django.contrib import admin

from settings.models import PushNotificationSetting


class PushNotificationSettingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(PushNotificationSetting, PushNotificationSettingAdmin)
