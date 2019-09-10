from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserJobHistorySerializer


class UserJobHistoryListView(APIView):
    """
    List job histories,
    create new job history
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        user_job_histories = request.user.job_histories
        serializer = UserJobHistorySerializer(user_job_histories, many=True)
        return Response(serializer.data)
