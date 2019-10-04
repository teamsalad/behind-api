from django.contrib import admin
from purchases.models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Purchase, PurchaseAdmin)
