from django.contrib import admin

from settings.models import PushNotificationSetting, AppVersion


class PushNotificationSettingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class AppVersionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(PushNotificationSetting, PushNotificationSettingAdmin)
admin.site.register(AppVersion, AppVersionAdmin)
