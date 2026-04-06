from django.db import models
from django.core.validators import MinValueValidator
from config.models import Location

BIKE_TYPES = (
    ('MTB', 'Mountain Bike'),
    ('Road', 'Road Bike'),
    ('Hybrid', 'Hybrid Bike'),
    ('Cruiser', 'Cruiser Bike'),
    ('BMX', 'BMX Bike'),
    ('Electric', 'Electric Bike'),
)

class Bike(models.Model):
    """Bike model for bike rental system"""
    BIKE_CONDITION = (
        ('New', 'New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    )
    
    name = models.CharField(max_length=200)
    bike_type = models.CharField(max_length=50, choices=BIKE_TYPES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(default=2024, validators=[MinValueValidator(2000)])
    
    # Location
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='bikes')
    
    # Pricing
    rental_price_hourly = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    rental_price_daily = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Details
    color = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    condition = models.CharField(max_length=20, choices=BIKE_CONDITION, default='Good')
    is_available = models.BooleanField(default=True)
    
    # Images
    image = models.ImageField(upload_to='bike_images/', blank=True, null=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['location', 'bike_type']),
            models.Index(fields=['is_available']),
        ]
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.location.name}"

    @property
    def city(self):
        return self.location.name
