import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from djmoney.money import Money

from behind import settings
from payments.models import Payment, STATUS, AUTHORITY
from purchases.models import Purchase, STATE
from users.forms import ConfirmPaymentTransactionForm
from users.models import User, UserAgreement


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'email', 'full_name',
        'username', 'role',
        'is_active', 'is_staff',
    )
    actions = ['confirm_payment_transaction']

    def confirm_payment_transaction(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = ConfirmPaymentTransactionForm(request.POST)
            timestamp = int(datetime.datetime.now().timestamp() * 10 ** 6)
            if form.is_valid():
                charging_points = form.cleaned_data['charging_points']
                for user in queryset:
                    payment = Payment.objects.create(
                        item_name='비하인드 수동 포인트 충전',
                        receipt_id='No receipts',
                        order_id=str(timestamp),
                        pg_alias='behind',
                        pg_name='Behind',
                        method_alias='bank',
                        method_name='계좌이체',
                        price=Money(charging_points, 'KRW'),
                        status=STATUS[1][0],
                        authority=AUTHORITY[0][0],
                        responded_at=datetime.datetime.now(),
                        user=user
                    )
                    Purchase.objects.create(
                        item=payment,
                        transaction_to=user,
                        transaction_from_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
                        amount=charging_points,
                        state=STATE[1][0]
                    )
                self.message_user(request, 'Successfully transacted points to selected user(s)')
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = ConfirmPaymentTransactionForm(initial={
                '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
            })
        opts = self.model._meta
        app_label = opts.app_label
        return render(
            request,
            'admin/users/confirm_payment_transaction_form.html',
            context={'users': queryset, 'form': form, "opts": opts, "app_label": app_label}
        )

    confirm_payment_transaction.short_description = 'Confirm user(s) payment transactions manually'


class UserAgreementAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'user', 'terms_of_use', 'privacy_policy',
        'marketing_information_reception',
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserAgreement, UserAgreementAdmin)
