from django.contrib import admin
from .models import Bike

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'bike_type', 'location', 'rental_price_hourly', 'is_available', 'created_at')
    list_filter = ('bike_type', 'location', 'is_available', 'created_at', 'condition')
    search_fields = ('name', 'brand', 'model')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'model', 'year', 'bike_type')
        }),
        ('Location & Pricing', {
            'fields': ('location', 'rental_price_hourly', 'rental_price_daily')
        }),
        ('Details', {
            'fields': ('color', 'description', 'condition', 'is_available', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
