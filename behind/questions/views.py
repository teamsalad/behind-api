from functools import reduce

from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from behind.pagination import CreatedAtCursorPagination
from questions.models import Question
from questions.permissions import IsQuestionOwnerOrReadOnly, IsAnswerOwnerOrReadOnly
from questions.serializers import (
    CreateQuestionSerializer,
    QuestionListSerializer,
    CreateAnswerSerializer,
    AnswerListSerializer)
from users.permissions import IsRoleEmployee


class QuestionFeedView(ListAPIView):
    """
    List questions that need to be answered
    """
    permission_classes = [IsAuthenticated, IsRoleEmployee]
    serializer_class = QuestionListSerializer
    pagination_class = CreatedAtCursorPagination

    def get_queryset(self):
        job_histories = self.request.user.job_histories.all()
        query = reduce(lambda x, y: x | y, [Q(company=item.company, job=item.job) for item in job_histories])
        return Question.objects.filter(query)


class QuestionListView(ListAPIView):
    """
    List questions with answers and
    create questions
    """
    permission_classes = [IsAuthenticated]
    pagination_class = CreatedAtCursorPagination

    def get_queryset(self):
        return self.request.user.questions.order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateQuestionSerializer
        return QuestionListSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class QuestionDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsQuestionOwnerOrReadOnly]
    serializer_class = QuestionListSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.request.user.questions.all()


class AnswerListView(ListAPIView):
    """
    List my answers and
    create answers
    """
    permission_classes = [IsAuthenticated, IsRoleEmployee]
    pagination_class = CreatedAtCursorPagination

    def get_queryset(self):
        return self.request.user.answers.order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAnswerSerializer
        return AnswerListSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AnswerDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsRoleEmployee, IsAnswerOwnerOrReadOnly]
    serializer_class = AnswerListSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.request.user.answers.all()
