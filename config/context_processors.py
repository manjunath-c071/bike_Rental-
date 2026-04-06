"""
Context processors for RideNova
Adds useful context variables to all templates
"""

from bikes.admin_utils import is_admin


def admin_context(request):
    """Add admin status to template context"""
    return {
        'is_admin': is_admin(request.user),
        'user_is_admin': is_admin(request.user),
    }
