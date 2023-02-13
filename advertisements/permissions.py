from rest_framework.permissions import BasePermission


class IsOwnerAndAuthenticatedOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator and bool(request.user and request.user.is_authenticated) or bool(request.user and request.user.is_staff):
            return True
        else:
            return False


class IsNotOwnerAndAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user != obj.creator and bool(request.user and request.user.is_authenticated):
            return True
        else:
            return False
