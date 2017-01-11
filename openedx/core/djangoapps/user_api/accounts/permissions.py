"""
Permissions classes for User accounts API views.
"""
from __future__ import unicode_literals

from rest_framework import permissions


class IsSuperUserOrCanDeactivateUser(permissions.BasePermission):
    """
    Grants access to AccountDeactivationView if the requesting user is a superuser
    or has the explicit permission to deactivate a User account.
    """
    PERMISSION_TO_DEACTIVATE_USER_ACCOUNT_NAME = 'student.can_deactivate_users'

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser or user.has_perm(self.PERMISSION_TO_DEACTIVATE_USER_ACCOUNT_NAME):
            return True
        return False
