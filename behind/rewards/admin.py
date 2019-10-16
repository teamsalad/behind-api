from django.contrib import admin

from rewards.models import Gifticon


class GifticonAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name', 'exchange', 'point_price', 'price', 'supplier',)


admin.site.register(Gifticon, GifticonAdmin)
