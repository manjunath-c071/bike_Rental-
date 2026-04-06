from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import UserProfile
from .forms import SignUpForm, LoginForm, UserProfileForm
from bookings.models import Booking

def signup_view(request):
    """User signup view with license details"""
    if request.user.is_authenticated:
        return redirect('bikes:bike_list')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                # Create profile with license info (also done in form.save but let's ensure)
                profile = user.profile
                
                # Auto login after signup
                # Authenticate using email
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                
                # Try to get user by email and authenticate
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                
                if user:
                    login(request, user)
                    messages.success(request, 'Account created successfully! Welcome to RideNova! 🎉')
                    return redirect('bikes:bike_list')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                # Clean up partially created user if needed
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, 'users/signup.html', context)


def login_view(request):
    """Custom email-based login view"""
    if request.user.is_authenticated:
        return redirect('bikes:bike_list')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                
                # Find user by email
                try:
                    user_obj = User.objects.get(email=email)
                    username = user_obj.username
                except User.DoesNotExist:
                    messages.error(request, 'Invalid email or password.')
                    return render(request, 'users/login.html', {'form': form})
                
                # Authenticate
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    remember_me = form.cleaned_data.get('remember_me')
                    if not remember_me:
                        # Session expires when browser closes
                        request.session.set_expiry(0)
                    
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    
                    # Redirect to next page or bikes list
                    next_page = request.GET.get('next')
                    return redirect(next_page) if next_page else redirect('bikes:bike_list')
                else:
                    messages.error(request, 'Invalid email or password.')
            except Exception as e:
                messages.error(request, f'Login error: {str(e)}')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'users/login.html', context)


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='users:login')
def dashboard_view(request):
    """User dashboard with profile, bookings, and license info"""
    profile = request.user.profile
    
    # Get all bookings with filtering
    bookings = request.user.bookings.all().order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Calculate booking statistics
    total_bookings = request.user.bookings.count()
    active_bookings = request.user.bookings.filter(status__in=['pending', 'confirmed']).count()
    completed_bookings = request.user.bookings.filter(status='completed').count()
    
    # Check license verification status
    license_verified = bool(profile.license_number and profile.license_document)
    
    # Get address info
    address = {
        'street': profile.address,
        'city': profile.city,
        'state': profile.state,
        'pincode': profile.pincode,
    }
    
    context = {
        'profile': profile,
        'bookings': bookings,
        'license_verified': license_verified,
        'address': address,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'status_filter': status_filter,
    }
    return render(request, 'users/dashboard.html', context)


@login_required(login_url='users:login')
def profile_view(request):
    """View user profile (redirects to dashboard)"""
    return redirect('users:dashboard')


@login_required(login_url='users:login')
def cancel_booking_view(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been cancelled successfully.')
    else:
        messages.warning(request, f'Cannot cancel {booking.get_status_display()} booking.')
    
    return redirect('users:dashboard')


@login_required(login_url='users:login')
def edit_profile_view(request):
    """Edit user profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('users:dashboard')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'users/edit_profile.html', context)
