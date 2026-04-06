from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'license_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'date_of_birth', 'profile_picture')
        }),
        ('Driving License', {
            'fields': ('license_number', 'license_issue_date', 'license_expiry_date', 'license_document', 'is_verified')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
