"""
Admin utilities for intra-page admin controls
Provides decorators and mixins to restrict access to admin features for logged-in admins only
"""

from functools import wraps
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def admin_required(view_func):
    """
    Decorator to ensure only admin users can access a view.
    Returns JSON response for AJAX requests and renders error page for regular requests.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            return HttpResponseForbidden('Authentication required')
        
        if not request.user.is_staff or not request.user.is_superuser:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Admin access required'
                }, status=403)
            return HttpResponseForbidden('Admin access required')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_ajax_required(view_func):
    """
    Decorator to ensure only admin users can access an AJAX endpoint.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        
        if not request.user.is_staff or not request.user.is_superuser:
            return JsonResponse({
                'success': False,
                'error': 'Admin access required'
            }, status=403)
        
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'Invalid request'
            }, status=400)
        
        return view_func(request, *args, **kwargs)
    return wrapper


class AdminUserMixin:
    """
    Mixin for class-based views to restrict access to admin users only.
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('Authentication required')
        
        if not request.user.is_staff or not request.user.is_superuser:
            return HttpResponseForbidden('Admin access required')
        
        return super().dispatch(request, *args, **kwargs)


def is_admin(user):
    """
    Check if user is an admin (superuser with staff status)
    """
    return user.is_authenticated and user.is_staff and user.is_superuser
