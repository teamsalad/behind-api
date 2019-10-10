from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from behind.pagination import CreatedAtCursorPagination
from questions.models import Question
from questions.serializers import (
    CreateQuestionSerializer,
    QuestionListSerializer,
    CreateAnswerSerializer,
    AnswerListSerializer)


class QuestionFeedView(ListAPIView):
    # TODO: Add role related permissions
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all().order_by('-created_at')
    pagination_class = CreatedAtCursorPagination


class QuestionListView(ListAPIView):
    """
    List questions with answers and
    create questions
    """
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionListSerializer
    lookup_field = 'id'

    # TODO: Add my resource permission 'isQuestionOwner'
    def get_queryset(self):
        return self.request.user.questions.all()


class AnswerListView(ListAPIView):
    """
    List my answers and
    create answers
    """
    # TODO: Add role related permissions
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnswerListSerializer
    lookup_field = 'id'

    # TODO: Add my resource permission 'isAnswerOwner'
    def get_queryset(self):
        return self.request.user.answers.all()
