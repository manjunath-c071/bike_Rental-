from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Booking


class BookingForm(forms.ModelForm):
    """Form for creating bike bookings"""
    
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'min': timezone.now().isoformat()
        }),
        label='Start Date & Time',
        help_text='When do you want to start your ride?'
    )
    
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label='End Date & Time',
        help_text='When will you return the bike?'
    )
    
    pickup_location = forms.ChoiceField(
        choices=Booking.LOCATION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Pickup Location'
    )
    
    return_location = forms.ChoiceField(
        choices=Booking.LOCATION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Return Location'
    )
    
    custom_pickup_location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Specify custom pickup location'
        }),
        label='Custom Pickup Location (Supplier name, address, etc.)'
    )
    
    custom_return_location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Specify custom return location'
        }),
        label='Custom Return Location (Supplier name, address, etc.)'
    )
    
    notes = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any special requests or notes?'
        }),
        label='Additional Notes'
    )
    
    insurance_opted = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Add Insurance (5% of rental cost)',
        help_text='Protect yourself with comprehensive bike damage coverage'
    )
    
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'pickup_location', 'return_location', 
                  'custom_pickup_location', 'custom_return_location', 'notes', 'insurance_opted']
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        # Validate dates
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('End date must be after start date.')
            
            # Minimum 30 minutes rental
            min_duration = start_date + timedelta(minutes=30)
            if end_date < min_duration:
                raise forms.ValidationError('Minimum rental duration is 30 minutes.')
            
            # Maximum 30 days rental
            max_duration = start_date + timedelta(days=30)
            if end_date > max_duration:
                raise forms.ValidationError('Maximum rental duration is 30 days.')
        
        # Check pickup location requirement
        if cleaned_data.get('pickup_location') == 'other' and not cleaned_data.get('custom_pickup_location'):
            raise forms.ValidationError('Please specify custom pickup location.')
        
        # Check return location requirement
        if cleaned_data.get('return_location') == 'other' and not cleaned_data.get('custom_return_location'):
            raise forms.ValidationError('Please specify custom return location.')
        
        return cleaned_data
