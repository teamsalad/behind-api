from django.contrib import admin

from settings.models import PushNotificationSetting, AppVersion


class PushNotificationSettingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('user', 'chat', 'answered', 'asked',)


class AppVersionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'name', 'code', 'device_type',
        'release_state', 'update_state',
    )


admin.site.register(PushNotificationSetting, PushNotificationSettingAdmin)
admin.site.register(AppVersion, AppVersionAdmin)
