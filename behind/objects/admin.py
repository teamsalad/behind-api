from django.contrib import admin

from objects.models import Object


class ObjectAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Object, ObjectAdmin)
