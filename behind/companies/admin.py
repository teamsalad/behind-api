from django.contrib import admin
from companies.models import Company, Job, UserJobHistory


class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name', 'email_domain',)


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title',)


class UserJobHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'user', 'company', 'job',
        'confirmed', 'confirmation_method',
        'confirmation_information',
    )


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(UserJobHistory, UserJobHistoryAdmin)
