from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "jobs"


class Company(models.Model):
    name = models.CharField(max_length=100)
    email_domain = models.CharField(max_length=100)
    jobs = models.ManyToManyField(Job)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "companies"
