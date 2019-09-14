from django.conf import settings
from django.db import models

METHODS = (
    (1, "email"),
    (2, "business_card"),
    (3, "proof_of_employment"),
)


class Job(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Job {self.title}'

    class Meta:
        db_table = "jobs"


class Company(models.Model):
    name = models.CharField(max_length=100)
    email_domain = models.CharField(max_length=100)
    jobs = models.ManyToManyField(Job)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Company {self.name} {self.email_domain}'

    class Meta:
        db_table = "companies"


class UserJobHistory(models.Model):
    confirmation_method = models.PositiveSmallIntegerField(
        choices=METHODS,
        default=METHODS[0][0]
    )
    confirmed = models.BooleanField(default=False)
    confirmation_information = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_histories'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def confirm(self):
        self.confirmed = True
        self.save()

    def __str__(self):
        return f'UserJobHistory {self.confirmation_information} {self.confirmed}'

    class Meta:
        db_table = "user_job_histories"
