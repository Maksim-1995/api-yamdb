from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение доступа только для администраторов."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение доступа для администраторов и только для чтения."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Разрешение доступа для автора, модератора, администратора и только для чтения."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
            or request.user.is_superuser
        )
