from django.contrib import admin

from questions.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
