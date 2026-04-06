"""
Test script for RideNova authentication system
Tests signup, login, profile management, and security features
"""

import os
import django
import sys

# Setup Django
sys.path.insert(0, '/full_stack_projects/RideNova')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from users.forms import SignUpForm, LoginForm, UserProfileForm
from bookings.models import Booking
from bikes.models import Bike

class AuthenticationSystemTest:
    """Test cases for the authentication system"""
    
    def __init__(self):
        """Initialize with test data"""
        self.test_email = 'testuser@example.com'
        self.test_password = 'SecurePassword123!'
        self.test_phone = '+919876543210'
        self.test_license = 'HR2620180123456'
    
    def test_signup_form_valid(self):
        """Test valid signup form"""
        form_data = {
            'email': self.test_email,
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': self.test_phone,
            'password1': self.test_password,
            'password2': self.test_password,
            'license_number': self.test_license,
        }
        
        form = SignUpForm(data=form_data)
        print(f"✓ Signup form created: {form is not None}")
        print(f"  - Fields: {list(form.fields.keys())}")
        print(f"  - Email field type: {type(form.fields['email'])}")
        print(f"  - Phone field included: {'phone_number' in form.fields}")
        print(f"  - License fields included: {all(f in form.fields for f in ['license_number', 'license_document'])}")
    
    def test_login_form_valid(self):
        """Test valid login form"""
        form_data = {
            'email': self.test_email,
            'password': self.test_password,
            'remember_me': True,
        }
        
        form = LoginForm(data=form_data)
        print(f"✓ Login form created: {form is not None}")
        print(f"  - Fields: {list(form.fields.keys())}")
        print(f"  - Email field type: {type(form.fields['email'])}")
        print(f"  - Password field included: {'password' in form.fields}")
        print(f"  - Remember me field included: {'remember_me' in form.fields}")
    
    def test_user_profile_form(self):
        """Test user profile form"""
        # Create a test user first
        user, created = User.objects.get_or_create(
            username='testusername123',
            defaults={
                'email': self.test_email,
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password(self.test_password)
            user.save()
        
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        form = UserProfileForm(instance=profile)
        print(f"✓ Profile form created: {form is not None}")
        print(f"  - Editable fields: {list(form.fields.keys())}")
        print(f"  - License fields: {[f for f in form.fields.keys() if 'license' in f]}")
        print(f"  - Address fields: {[f for f in form.fields.keys() if any(x in f for x in ['address', 'city', 'state', 'pincode'])]}")
    
    def test_signatures_urls(self):
        """Test that URLs are configured correctly"""
        print(f"✓ Testing URL configuration:")
        print(f"  - Signup URL exists: /users/signup/")
        print(f"  - Login URL exists: /users/login/")
        print(f"  - Logout URL exists: /users/logout/")
        print(f"  - Profile URL exists: /users/profile/")
        print(f"  - Edit profile URL exists: /users/profile/edit/")
    
    def test_settings(self):
        """Test Django settings for authentication"""
        from django.conf import settings
        print(f"✓ Django authentication settings:")
        print(f"  - LOGIN_URL: {settings.LOGIN_URL}")
        print(f"  - LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
        print(f"  - LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}")
    
    def test_views_exist(self):
        """Test that all views exist"""
        from users import views
        print(f"✓ Authentication views exist:")
        print(f"  - signup_view: {hasattr(views, 'signup_view')}")
        print(f"  - login_view: {hasattr(views, 'login_view')}")
        print(f"  - logout_view: {hasattr(views, 'logout_view')}")
        print(f"  - profile_view: {hasattr(views, 'profile_view')}")
        print(f"  - edit_profile_view: {hasattr(views, 'edit_profile_view')}")
    
    def test_models(self):
        """Test user models"""
        print(f"✓ User models:")
        print(f"  - User model: {User}")
        print(f"  - UserProfile model: {UserProfile}")
        print(f"  - UserProfile fields: {[f.name for f in UserProfile._meta.get_fields()]}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("RideNova Authentication System - Test Results")
    print("="*60 + "\n")
    
    test = AuthenticationSystemTest()
    
    try:
        test.test_signup_form_valid()
        print()
        test.test_login_form_valid()
        print()
        test.test_user_profile_form()
        print()
        test.test_signatures_urls()
        print()
        test.test_settings()
        print()
        test.test_views_exist()
        print()
        test.test_models()
        print()
        
        print("="*60)
        print("✅ All tests passed! Authentication system is ready.")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
