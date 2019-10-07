from django.contrib import admin

from behind import settings
from purchases.models import Purchase, STATE
from users.models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    actions = ['give_10k_points', 'give_100k_points']

    def give_10k_points(self, request, queryset):
        for user in queryset:
            user.incomings.add(Purchase.objects.create(
                amount=10000,
                item_id=1,  # TODO: Fix the numbers in the near future.
                item_type_id=18,
                transaction_from_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
                transaction_to=user,
                state=STATE[1][0]
            ))
        self.message_user(request, "Successfully gave away 10k points to selected users")

    give_10k_points.short_description = 'Give 10k points to user(s)'

    def give_100k_points(self, request, queryset):
        for user in queryset:
            user.incomings.add(Purchase.objects.create(
                amount=100000,
                item_id=1,  # TODO: Fix the numbers in the near future.
                item_type_id=18,
                transaction_from_id=settings.TRANSACTION_STAGING_ACCOUNT_ID,
                transaction_to=user,
                state=STATE[1][0]
            ))
        self.message_user(request, "Successfully gave away 100k points to selected users")

    give_100k_points.short_description = 'Give 100k points to user(s)'


admin.site.register(User, UserAdmin)
