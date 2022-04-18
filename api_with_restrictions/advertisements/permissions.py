from rest_framework.permissions import BasePermission


class IsAdvOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        return obj.creator == request.user
