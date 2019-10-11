from rest_framework.permissions import BasePermission

from users.models import ROLES


class IsRoleEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == ROLES[1][0]
