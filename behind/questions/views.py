from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from questions.models import Question
from questions.serializers import (
    CreateQuestionSerializer,
    QuestionSerializer,
    CreateAnswerSerializer,
    AnswerSerializer,
)


class QuestionFeedView(ListAPIView):
    # TODO: Add role related permissions
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionListView(ListAPIView):
    """
    List questions with answers and
    create questions
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.questions.all()

    def get_serializer_context(self):
        context = (
            super(QuestionListView, self).get_serializer_context()
        )
        context.update({
            'current_user': self.request.user,
        })
        return context

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateQuestionSerializer
        return QuestionSerializer

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
    serializer_class = QuestionSerializer
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

    def get_queryset(self):
        return self.request.user.answers.all()

    def get_serializer_context(self):
        context = (
            super(AnswerListView, self).get_serializer_context()
        )
        context.update({
            'current_user': self.request.user,
        })
        return context

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAnswerSerializer
        return AnswerSerializer

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
    serializer_class = AnswerSerializer
    lookup_field = 'id'

    # TODO: Add my resource permission 'isAnswerOwner'
    def get_queryset(self):
        return self.request.user.answers.all()
