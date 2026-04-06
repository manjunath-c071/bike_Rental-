from django.db import models
from django.core.validators import MinValueValidator


class Location(models.Model):
    """Location/City model for bike rental locations"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=10, default='🏙️', help_text="Emoji icon for the location")
    color = models.CharField(max_length=7, default='#FF6B6B', help_text="Hex color code")
    image = models.ImageField(upload_to='location_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Location details
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    
    def __str__(self):
        return self.name