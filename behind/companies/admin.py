from django.contrib import admin
from companies.models import Company, Job, UserJobHistory


class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class UserJobHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(UserJobHistory, UserJobHistoryAdmin)
