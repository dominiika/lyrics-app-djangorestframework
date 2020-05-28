from rest_framework import permissions


class UpdateOwnModel(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class DeleteOwnModel(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method != "DELETE":
            return True

        return obj.user.id == request.user.id
