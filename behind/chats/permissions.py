from rest_framework.permissions import BasePermission


class IsChatRoomParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(user=request.user).exists()
