from django.contrib import admin
from companies.models import Company, Job, UserJobHistory

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(UserJobHistory)
