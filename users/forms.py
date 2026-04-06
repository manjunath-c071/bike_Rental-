from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
import re

class SignUpForm(UserCreationForm):
    """Comprehensive user signup form with license details"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        help_text='We\'ll use this to verify your account'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+91 XXXXX XXXXX',
            'type': 'tel'
        }),
        help_text='10-15 digit phone number'
    )
    
    license_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., HR26 20180123456'
        }),
        help_text='Your driving license number'
    )
    
    license_document = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*,.pdf'
        }),
        help_text='Upload a photo or PDF of your driving license'
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
        self.fields['password1'].help_text = 'Must be at least 8 characters with uppercase, lowercase, and numbers'
        self.fields['password2'].help_text = 'Enter the same password again'
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_phone_number(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?1?\d{9,15}$', phone.replace(' ', '').replace('-', '')):
            raise forms.ValidationError('Please enter a valid phone number (10-15 digits).')
        return phone
    
    def clean_license_number(self):
        """Validate license number format"""
        license_num = self.cleaned_data.get('license_number')
        if not license_num or len(license_num) < 5:
            raise forms.ValidationError('Please enter a valid driving license number.')
        return license_num
    
    def clean_license_document(self):
        """Validate license document"""
        doc = self.cleaned_data.get('license_document')
        if doc:
            # Check file size (max 5MB)
            if doc.size > 5 * 1024 * 1024:
                raise forms.ValidationError('License document must be less than 5MB.')
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
            if doc.content_type not in allowed_types:
                raise forms.ValidationError('License document must be an image (JPEG/PNG) or PDF.')
        return doc
    
    def save(self, commit=True):
        """Save user and create profile"""
        user = super().save(commit=False)
        # Use email as username for easier login
        user.username = self.cleaned_data['email'].split('@')[0] + str(User.objects.count())
        
        if commit:
            user.save()
            # Create profile with license info
            profile = UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                license_number=self.cleaned_data['license_number'],
                license_document=self.cleaned_data['license_document']
            )
        return user


class LoginForm(forms.Form):
    """Custom login form using email instead of username"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autofocus': True
        }),
        label='Email Address'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Remember me'
    )


class UserProfileForm(forms.ModelForm):
    """User profile form for editing profile details"""
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'date_of_birth', 'profile_picture',
            'license_number', 'license_issue_date', 'license_expiry_date',
            'license_document', 'address', 'city', 'state', 'pincode'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., HR26 20180123456'
            }),
            'license_issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'license_expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'license_document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal code'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        """Save profile and update user info"""
        profile = super().save(commit=False)
        # Update user fields
        profile.user.first_name = self.cleaned_data.get('first_name', '')
        profile.user.last_name = self.cleaned_data.get('last_name', '')
        profile.user.email = self.cleaned_data.get('email', profile.user.email)
        
        if commit:
            profile.user.save()
            profile.save()
        return profile
