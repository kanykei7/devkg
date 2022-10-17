from rest_framework import permissions


class VacancyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.company.user == request.user:
            return True
        return False

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
