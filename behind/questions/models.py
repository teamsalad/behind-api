from django.db import models

from behind import settings
from companies.models import Company, Job


class Question(models.Model):
    content = models.TextField()
    questioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions'
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

    def __str__(self):
        return f'Question {self.id} {self.content}'

    class Meta:
        db_table = "questions"


class Answer(models.Model):
    content = models.TextField()
    answerer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Answer {self.id} {self.content}'

    class Meta:
        db_table = "answers"
