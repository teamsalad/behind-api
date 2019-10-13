from django.contrib import admin

from rewards.models import Gifticon


class GifticonAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Gifticon, GifticonAdmin)
