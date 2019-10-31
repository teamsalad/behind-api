from django.contrib import admin
from companies.models import Company, Job, UserJobHistory


class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name', 'email_domain',)
    list_filter = ('email_domain',)
    search_fields = ('name', 'email_domain',)


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title',)
    search_fields = ('title',)


class UserJobHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = (
        'user', 'company', 'job',
        'confirmed', 'confirmation_method',
        'confirmation_information',
    )
    search_fields = ('company__name', 'company__email_domain',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(UserJobHistory, UserJobHistoryAdmin)
