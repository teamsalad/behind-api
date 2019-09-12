from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView

from .serializers import (
    UserJobHistorySerializer,
    CreateUserJobHistorySerializer,
)


class UserJobHistoryListView(ListAPIView):
    """
    List job histories,
    create new job history
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.job_histories.all()

    def get_serializer_context(self):
        context = (
            super(UserJobHistoryListView, self)
            .get_serializer_context()
        )
        context.update({
            'current_user': self.request.user,
        })
        return context

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserJobHistorySerializer
        return UserJobHistorySerializer

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
