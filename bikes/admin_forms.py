from django import forms
from bikes.models import Bike
from bookings.models import Booking
from django.contrib.auth.models import User
from users.models import UserProfile
from config.models import Location


class BikeAdminForm(forms.ModelForm):
    """Form for adding/editing bikes in admin panel"""
    
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True),
        empty_label="Select Location",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Bike
        fields = ['name', 'brand', 'model', 'year', 'bike_type', 'location', 
                  'rental_price_hourly', 'rental_price_daily', 'is_available', 
                  'condition', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bike Name'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand (e.g., Hero, Bajaj)'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model Name'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year of Manufacture'
            }),
            'bike_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rental_price_hourly': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hourly Rate (₹)',
                'step': '0.01'
            }),
            'rental_price_daily': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Daily Rate (₹)',
                'step': '0.01'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        hourly_rate = cleaned_data.get('rental_price_hourly')
        daily_rate = cleaned_data.get('rental_price_daily')
        
        if hourly_rate and daily_rate and hourly_rate < 0:
            raise forms.ValidationError("Please enter valid rental prices")
        
        return cleaned_data


class BookingStatusForm(forms.ModelForm):
    """Form for updating booking status in admin panel"""
    
    class Meta:
        model = Booking
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Admin notes about this booking'
            }),
        }


class UserProfileAdminForm(forms.ModelForm):
    """Form for managing user profiles in admin panel"""
    
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'address', 'city', 
                  'state', 'pincode', 'is_verified', 'profile_picture']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXXXXXXX'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pincode'
            }),
            'is_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


class UserPermissionForm(forms.Form):
    """Form for managing user permissions in admin panel"""
    
    ROLE_CHOICES = [
        ('user', 'Regular User'),
        ('staff', 'Staff/Admin'),
        ('superuser', 'Superuser'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


# Payment Forms
from payments.models import Payment


class PaymentRefundForm(forms.Form):
    """Form for refunding payments by admin"""
    
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Reason for refund'
        }),
        required=True
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Additional notes (optional)'
        }),
        required=False
    )

