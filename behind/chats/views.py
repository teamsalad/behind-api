from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from chats.models import ChatRoom
from chats.permissions import IsChatRoomParticipant
from chats.serializers import CreateChatRoomSerializer, ChatRoomSerializer


class ChatRoomCreateView(CreateAPIView):
    """Create chat room and participants"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateChatRoomSerializer

    def post(self, request, format=None, **kwargs):
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


class ChatRoomDetailView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsChatRoomParticipant]
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()
    lookup_field = 'id'
