from django.contrib import admin

from payments.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'item_name', 'user', 'price', 'pg_name',
        'method_name', 'status', 'authority',
    )


admin.site.register(Payment, PaymentAdmin)
