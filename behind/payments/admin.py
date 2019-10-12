from django.contrib import admin

from payments.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Payment, PaymentAdmin)
