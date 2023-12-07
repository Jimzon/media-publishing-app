from rest_framework.permissions import SAFE_METHODS, BasePermission


class ArticlePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_editor

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return obj.writer_id == request.user.id or obj.writer_id == request.user.id
