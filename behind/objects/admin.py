from django.contrib import admin

from objects.models import Object


class ObjectAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('link_alias', 'type', 'state', 'object',)


admin.site.register(Object, ObjectAdmin)
