from django.db import models
from django.contrib.auth.models import User
from bikes.models import Bike
from django.utils import timezone

class Booking(models.Model):
    """Booking model for bike rentals"""
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    LOCATION_CHOICES = (
        ('airport', 'Airport'),
        ('railway', 'Railway Station'),
        ('bus_stand', 'Bus Stand'),
        ('city_center', 'City Center'),
        ('mall', 'Shopping Mall'),
        ('hotel', 'Hotel'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='bookings')
    
    # Booking dates and times
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Location details
    pickup_location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    return_location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    custom_pickup_location = models.CharField(max_length=255, blank=True, help_text="For 'Other' location")
    custom_return_location = models.CharField(max_length=255, blank=True, help_text="For 'Other' location")
    
    # Pricing
    total_hours = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    
    # Additional details
    notes = models.TextField(blank=True)
    is_helmet_required = models.BooleanField(default=True)
    insurance_opted = models.BooleanField(default=False)
    insurance_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.bike}"
    
    def calculate_cost(self):
        """Calculate booking cost"""
        if self.start_date and self.end_date:
            duration = (self.end_date - self.start_date).total_seconds() / 3600
            self.total_hours = duration
            self.hourly_rate = self.bike.rental_price_hourly
            self.total_cost = self.hourly_rate * duration
            
            if self.insurance_opted:
                # Insurance is typically 5% of rental cost
                self.insurance_amount = self.total_cost * 0.05
                self.total_cost += self.insurance_amount
            
            return self.total_cost
        return 0
    
    def save(self, *args, **kwargs):
        """Calculate cost before saving"""
        self.calculate_cost()
        super().save(*args, **kwargs)
