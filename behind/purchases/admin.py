from django.contrib import admin
from purchases.models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'transaction_from', 'transaction_to',
        'amount', 'item', 'type', 'state',
    )


admin.site.register(Purchase, PurchaseAdmin)
