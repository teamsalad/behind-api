from django.contrib import admin

from questions.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('content', 'questioner', 'company', 'job',)


class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('content', 'answerer', 'question')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
