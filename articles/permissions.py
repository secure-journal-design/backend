from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

class IsArticleEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='article_editors').exists()