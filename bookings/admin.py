from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bike', 'status', 'start_date', 'end_date', 'total_cost', 'created_at')
    list_filter = ('status', 'start_date', 'created_at', 'bike__location')
    search_fields = ('user__username', 'bike__name', 'id')
    readonly_fields = ('total_hours', 'total_cost', 'insurance_amount', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User & Bike', {
            'fields': ('user', 'bike')
        }),
        ('Booking Dates', {
            'fields': ('start_date', 'end_date', 'total_hours')
        }),
        ('Locations', {
            'fields': ('pickup_location', 'custom_pickup_location', 'return_location', 'custom_return_location')
        }),
        ('Pricing & Insurance', {
            'fields': ('hourly_rate', 'total_cost', 'is_helmet_required', 'insurance_opted', 'insurance_amount')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Calculate cost before saving"""
        obj.calculate_cost()
        super().save_model(request, obj, form, change)
