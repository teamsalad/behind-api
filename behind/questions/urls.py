from django.urls import path

from questions.views import (
    QuestionListView,
    QuestionDetailView,
)

urlpatterns = [
    path('', QuestionListView.as_view()),
    path('<int:id>', QuestionDetailView.as_view())
]
