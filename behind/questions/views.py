from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from questions.serializers import CreateQuestionSerializer, QuestionSerializer


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

    def get_queryset(self):
        return self.request.user.questions.all()
