from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from bikes.models import Bike
from bookings.models import Booking
from users.models import UserProfile
from config.models import Location
from bikes.admin_forms import BikeAdminForm, BookingStatusForm, UserProfileAdminForm, UserPermissionForm
from django.db.models import Count, Sum, Q, F
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import Http404


@staff_member_required(login_url='users:login')
def admin_dashboard(request):
    """Admin dashboard with comprehensive statistics and reports"""
    # Statistics
    total_users = User.objects.count()
    total_bikes = Bike.objects.count()
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(status__in=['pending', 'confirmed', 'active']).count()
    total_revenue = Booking.objects.filter(status='completed').aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    # Revenue this month
    today = date.today()
    first_day = today.replace(day=1)
    month_revenue = Booking.objects.filter(
        status='completed',
        created_at__gte=first_day
    ).aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related('user', 'bike').order_by('-created_at')[:10]
    
    # Bookings by status
    bookings_by_status = Booking.objects.values('status').annotate(count=Count('id'))
    
    # Top bikes
    top_bikes = Bike.objects.annotate(booking_count=Count('bookings')).order_by('-booking_count')[:5]
    
    # Average rating (if available)
    available_bikes_count = Bike.objects.filter(is_available=True).count()
    unavailable_bikes_count = Bike.objects.filter(is_available=False).count()
    
    # Upcoming bookings (next 7 days)
    seven_days_later = timezone.now() + timedelta(days=7)
    upcoming_bookings = Booking.objects.filter(
        start_date__lte=seven_days_later,
        status__in=['pending', 'confirmed']
    ).count()
    
    context = {
        'total_users': total_users,
        'total_bikes': total_bikes,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'total_revenue': total_revenue,
        'month_revenue': month_revenue,
        'available_bikes': available_bikes_count,
        'unavailable_bikes': unavailable_bikes_count,
        'upcoming_bookings': upcoming_bookings,
        'recent_bookings': recent_bookings,
        'bookings_by_status': bookings_by_status,
        'top_bikes': top_bikes,
    }
    
    return render(request, 'admin/dashboard.html', context)


# ============================================
# BIKE MANAGEMENT VIEWS
# ============================================

@staff_member_required(login_url='users:login')
def admin_bikes(request):
    """List all bikes with filters and pagination"""
    bikes = Bike.objects.all().order_by('-created_at')
    
    # Filter by city
    city_filter = request.GET.get('city')
    if city_filter:
        bikes = bikes.filter(location__name=city_filter)
    
    # Filter by bike type
    type_filter = request.GET.get('bike_type')
    if type_filter:
        bikes = bikes.filter(bike_type=type_filter)
    
    # Filter by availability
    availability = request.GET.get('availability')
    if availability == 'available':
        bikes = bikes.filter(is_available=True)
    elif availability == 'unavailable':
        bikes = bikes.filter(is_available=False)
    
    # Search by name/brand/model
    search = request.GET.get('search')
    if search:
        bikes = bikes.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(bikes, 20)
    page = request.GET.get('page', 1)
    bikes_page = paginator.get_page(page)
    
    # Get unique values for filters
    cities = Location.objects.filter(is_active=True).values_list('name', flat=True).order_by('name')
    bike_types = Bike._meta.get_field('bike_type').choices
    
    context = {
        'bikes': bikes_page,
        'cities': cities,
        'bike_types': bike_types,
        'current_city': city_filter,
        'current_type': type_filter,
        'current_availability': availability,
        'search_query': search,
    }
    return render(request, 'admin/bikes.html', context)


@staff_member_required(login_url='users:login')
def admin_bike_create(request):
    """Add a new bike"""
    if request.method == 'POST':
        # Check if it's an AJAX request
        if request.headers.get('Content-Type') == 'application/json' or request.POST.get('ajax') == 'true':
            from django.http import JsonResponse
            form = BikeAdminForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    bike = form.save()
                    return JsonResponse({
                        'success': True,
                        'bike': {
                            'id': bike.id,
                            'name': bike.name,
                            'bike_type_display': bike.get_bike_type_display(),
                            'city': bike.city,
                            'rental_price_daily': str(bike.rental_price_daily),
                            'is_available': bike.is_available
                        }
                    })
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            # Regular form submission
            form = BikeAdminForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    bike = form.save()
                    messages.success(request, f'Bike "{bike.name}" added successfully!')
                    return redirect('admin_dashboard:bikes')
                except Exception as e:
                    messages.error(request, f'Error creating bike: {str(e)}')
    else:
        form = BikeAdminForm()
    
    context = {'form': form, 'title': 'Add New Bike'}
    return render(request, 'admin/bike_form.html', context)


@staff_member_required(login_url='users:login')
def admin_bike_edit(request, bike_id):
    """Edit an existing bike"""
    bike = get_object_or_404(Bike, id=bike_id)
    
    if request.method == 'POST':
        # Check if it's an AJAX request for inline editing
        if request.headers.get('Content-Type') == 'application/json' or request.POST.get('ajax') == 'true':
            from django.http import JsonResponse
            import json
            
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
                field = data.get('field')
                value = data.get('value')
            else:
                field = request.POST.get('field')
                value = request.POST.get('value')
            
            if field and value is not None:
                try:
                    # Update the specific field
                    if field == 'name':
                        bike.name = value
                    elif field == 'bike_type':
                        bike.bike_type = value
                    elif field == 'location':
                        # For location, we need to find the Location object by name
                        try:
                            location = Location.objects.get(name=value, is_active=True)
                            bike.location = location
                        except Location.DoesNotExist:
                            return JsonResponse({'success': False, 'error': f'Location "{value}" not found'})
                    elif field == 'rental_price_daily':
                        bike.rental_price_daily = float(value)
                    else:
                        return JsonResponse({'success': False, 'error': f'Field {field} not supported for inline editing'})
                    
                    bike.save()
                    
                    # Return the updated display value
                    display_value = value
                    if field == 'bike_type':
                        type_labels = {
                            'MTB': 'Mountain Bike',
                            'Road': 'Road Bike',
                            'Hybrid': 'Hybrid Bike',
                            'Cruiser': 'Cruiser Bike',
                            'BMX': 'BMX Bike',
                            'Electric': 'Electric Bike'
                        }
                        display_value = type_labels.get(value, value)
                    elif field == 'rental_price_daily':
                        display_value = f"₹{value}"
                    
                    return JsonResponse({
                        'success': True,
                        'display_value': display_value
                    })
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            else:
                return JsonResponse({'success': False, 'error': 'Missing field or value'})
        else:
            # Regular form submission
            form = BikeAdminForm(request.POST, request.FILES, instance=bike)
            if form.is_valid():
                try:
                    bike = form.save()
                    messages.success(request, f'Bike "{bike.name}" updated successfully!')
                    return redirect('admin_dashboard:bike_detail', bike_id=bike.id)
                except Exception as e:
                    messages.error(request, f'Error updating bike: {str(e)}')
    else:
        form = BikeAdminForm(instance=bike)
    
    context = {'form': form, 'bike': bike, 'title': 'Edit Bike'}
    return render(request, 'admin/bike_form.html', context)


@staff_member_required(login_url='users:login')
def admin_bike_delete(request, bike_id):
    """Delete a bike"""
    bike = get_object_or_404(Bike, id=bike_id)
    
    if request.method == 'POST':
        # Check if it's an AJAX request
        if request.headers.get('Content-Type') == 'application/json' or request.POST.get('ajax') == 'true':
            from django.http import JsonResponse
            
            bike_name = bike.name
            # Check if bike has active bookings
            active_bookings = bike.bookings.filter(status__in=['pending', 'confirmed', 'active']).count()
            
            if active_bookings > 0:
                return JsonResponse({
                    'success': False, 
                    'error': f'Cannot delete bike with active bookings ({active_bookings} active booking(s))'
                })
            
            try:
                bike.delete()
                return JsonResponse({
                    'success': True,
                    'message': f'Bike "{bike_name}" deleted successfully!'
                })
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            # Regular form submission
            bike_name = bike.name
            # Check if bike has active bookings
            active_bookings = bike.bookings.filter(status__in=['pending', 'confirmed', 'active']).count()
            
            if active_bookings > 0:
                messages.error(request, f'Cannot delete bike with active bookings ({active_bookings} active booking(s))')
                return redirect('admin_dashboard:bike_detail', bike_id=bike.id)
            
            try:
                bike.delete()
                messages.success(request, f'Bike "{bike_name}" deleted successfully!')
                return redirect('admin_dashboard:bikes')
            except Exception as e:
                messages.error(request, f'Error deleting bike: {str(e)}')
                return redirect('admin_dashboard:bike_detail', bike_id=bike.id)
    
    context = {'bike': bike}
    return render(request, 'admin/bike_confirm_delete.html', context)


@staff_member_required(login_url='users:login')
def admin_bike_detail(request, bike_id):
    """View bike details and statistics"""
    bike = get_object_or_404(Bike, id=bike_id)
    bookings = bike.bookings.select_related('user').order_by('-created_at')[:20]
    
    # Statistics
    total_bookings = bike.bookings.count()
    completed_bookings = bike.bookings.filter(status='completed').count()
    revenue = bike.bookings.filter(status='completed').aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    context = {
        'bike': bike,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'revenue': revenue,
    }
    return render(request, 'admin/bike_detail.html', context)


# ============================================
# BOOKING MANAGEMENT VIEWS
# ============================================

@staff_member_required(login_url='users:login')
def admin_bookings(request):
    """List all bookings with filters and pagination"""
    bookings = Booking.objects.select_related('user', 'bike').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        bookings = bookings.filter(created_at__gte=start_date)
    if end_date:
        bookings = bookings.filter(created_at__lte=end_date)
    
    # Search by user email
    search = request.GET.get('search')
    if search:
        bookings = bookings.filter(
            Q(user__email__icontains=search) |
            Q(bike__name__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(bookings, 25)
    page = request.GET.get('page', 1)
    bookings_page = paginator.get_page(page)
    
    # Get unique statuses
    statuses = Booking._meta.get_field('status').choices
    
    context = {
        'bookings': bookings_page,
        'statuses': statuses,
        'current_status': status_filter,
        'search_query': search,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'admin/bookings.html', context)


@staff_member_required(login_url='users:login')
def admin_booking_detail(request, booking_id):
    """View and manage a specific booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Booking updated successfully!')
                return redirect('admin_dashboard:booking_detail', booking_id=booking.id)
            except Exception as e:
                messages.error(request, f'Error updating booking: {str(e)}')
    else:
        form = BookingStatusForm(instance=booking)
    
    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'admin/booking_detail.html', context)


@staff_member_required(login_url='users:login')
def admin_booking_cancel(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Booking cancelled successfully!')
        else:
            messages.error(request, f'Cannot cancel booking with status "{booking.get_status_display()}"')
        
        return redirect('admin_dashboard:booking_detail', booking_id=booking.id)
    
    context = {'booking': booking}
    return render(request, 'admin/booking_confirm_cancel.html', context)


# ============================================
# USER MANAGEMENT VIEWS
# ============================================

@staff_member_required(login_url='users:login')
def admin_users(request):
    """List all users with filters and pagination"""
    users = User.objects.prefetch_related('profile').order_by('-date_joined')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'staff':
        users = users.filter(is_staff=True)
    
    # Filter by verification
    verified_filter = request.GET.get('verified')
    if verified_filter == 'verified':
        users = users.filter(profile__is_verified=True)
    elif verified_filter == 'unverified':
        users = users.filter(profile__is_verified=False)
    
    # Search by email/name
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(users, 25)
    page = request.GET.get('page', 1)
    users_page = paginator.get_page(page)
    
    context = {
        'users': users_page,
        'current_status': status_filter,
        'verified_filter': verified_filter,
        'search_query': search,
    }
    return render(request, 'admin/users.html', context)


@staff_member_required(login_url='users:login')
def admin_user_detail(request, user_id):
    """View and manage user details"""
    user = get_object_or_404(User, id=user_id)
    bookings = user.bookings.order_by('-created_at')[:20]
    
    # Statistics
    total_bookings = user.bookings.count()
    completed_bookings = user.bookings.filter(status='completed').count()
    total_spent = user.bookings.filter(status='completed').aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    context = {
        'profile_user': user,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'total_spent': total_spent,
    }
    return render(request, 'admin/user_detail.html', context)


@staff_member_required(login_url='users:login')
def admin_user_edit(request, user_id):
    """Edit user profile and permissions"""
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    
    if request.method == 'POST':
        # Update user profile
        profile_form = UserProfileAdminForm(request.POST, request.FILES, instance=profile)
        perm_form = UserPermissionForm(request.POST)
        
        if profile_form.is_valid() and perm_form.is_valid():
            try:
                # Update profile
                profile_form.save()
                
                # Update user permissions
                role = perm_form.cleaned_data.get('role')
                user.is_active = perm_form.cleaned_data.get('is_active', True)
                
                if role == 'staff':
                    user.is_staff = True
                    user.is_superuser = False
                elif role == 'superuser':
                    user.is_staff = True
                    user.is_superuser = True
                else:
                    user.is_staff = False
                    user.is_superuser = False
                
                # Update user name and email from form
                user.first_name = profile_form.cleaned_data.get('first_name', '')
                user.last_name = profile_form.cleaned_data.get('last_name', '')
                user.email = profile_form.cleaned_data.get('email', user.email)
                user.save()
                
                messages.success(request, 'User updated successfully!')
                return redirect('admin_dashboard:user_detail', user_id=user.id)
            except Exception as e:
                messages.error(request, f'Error updating user: {str(e)}')
    else:
        profile_form = UserProfileAdminForm(instance=profile)
        # Determine current role
        if user.is_superuser:
            current_role = 'superuser'
        elif user.is_staff:
            current_role = 'staff'
        else:
            current_role = 'user'
        
        perm_form = UserPermissionForm(initial={
            'role': current_role,
            'is_active': user.is_active
        })
        
        # Populate name and email fields
        profile_form.initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
    
    context = {
        'profile_form': profile_form,
        'perm_form': perm_form,
        'profile_user': user,
    }
    return render(request, 'admin/user_form.html', context)


# ============================================
# REPORTS & ANALYTICS VIEWS
# ============================================

@staff_member_required(login_url='users:login')
def admin_reports(request):
    """View comprehensive reports and analytics"""
    
    # Date filters
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Revenue analytics
    bookings_in_period = Booking.objects.filter(
        created_at__gte=start_date,
        status='completed'
    )
    
    total_revenue_period = bookings_in_period.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    bookings_count_period = bookings_in_period.count()
    avg_booking_value = total_revenue_period / bookings_count_period if bookings_count_period > 0 else 0
    
    # Revenue by city
    revenue_by_city = Booking.objects.filter(
        created_at__gte=start_date,
        status='completed'
    ).annotate(
        city=F('bike__location__name')
    ).values('city').annotate(
        revenue=Sum('total_cost'),
        count=Count('id')
    ).order_by('-revenue')
    
    # Revenue by bike type
    revenue_by_type = Booking.objects.filter(
        created_at__gte=start_date,
        status='completed'
    ).values('bike__bike_type').annotate(
        revenue=Sum('total_cost'),
        count=Count('id')
    ).order_by('-revenue')
    
    # Top users by spending
    top_users = User.objects.filter(
        bookings__created_at__gte=start_date,
        bookings__status='completed'
    ).annotate(
        total_spent=Sum('bookings__total_cost'),
        bookings_count=Count('bookings')
    ).order_by('-total_spent')[:10]
    
    # Booking status summary
    status_summary = Booking.objects.filter(
        created_at__gte=start_date
    ).values('status').annotate(count=Count('id'))
    
    # User growth
    new_users = User.objects.filter(
        date_joined__gte=start_date
    ).count()
    
    # Bike utilization
    total_bikes_in_period = Bike.objects.count()
    utilized_bikes = Bike.objects.filter(
        bookings__created_at__gte=start_date
    ).distinct().count()
    
    context = {
        'days': days,
        'start_date': start_date,
        'total_revenue_period': total_revenue_period,
        'bookings_count_period': bookings_count_period,
        'avg_booking_value': round(avg_booking_value, 2),
        'revenue_by_city': revenue_by_city,
        'revenue_by_type': revenue_by_type,
        'top_users': top_users,
        'status_summary': status_summary,
        'new_users': new_users,
        'total_bikes': total_bikes_in_period,
        'utilized_bikes': utilized_bikes,
    }
    
    return render(request, 'admin/reports.html', context)


# ============================================
# LOCATION MANAGEMENT VIEWS
# ============================================

@staff_member_required(login_url='users:login')
def admin_locations(request):
    """List all locations with management options"""
    locations = Location.objects.all().order_by('name')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        locations = locations.filter(is_active=True)
    elif status_filter == 'inactive':
        locations = locations.filter(is_active=False)

    # Search by name
    search = request.GET.get('search')
    if search:
        locations = locations.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'locations': locations,
        'current_status': status_filter,
        'search_query': search,
    }
    return render(request, 'admin/locations.html', context)


@staff_member_required(login_url='users:login')
def admin_location_create(request):
    """Add a new location"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        icon = request.POST.get('icon', '🏙️')
        color = request.POST.get('color', '#FF6B6B')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        image = request.FILES.get('image')

        try:
            location = Location.objects.create(
                name=name,
                description=description,
                icon=icon,
                color=color,
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
                image=image
            )
            messages.success(request, f'Location "{location.name}" added successfully!')
            return redirect('admin_dashboard:locations')
        except Exception as e:
            messages.error(request, f'Error creating location: {str(e)}')
    else:
        # Pre-populate with some defaults
        pass

    return render(request, 'admin/location_form.html', {'title': 'Add New Location'})


@staff_member_required(login_url='users:login')
def admin_location_edit(request, location_id):
    """Edit an existing location"""
    location = get_object_or_404(Location, id=location_id)

    if request.method == 'POST':
        location.name = request.POST.get('name')
        location.description = request.POST.get('description', '')
        location.icon = request.POST.get('icon', '🏙️')
        location.color = request.POST.get('color', '#FF6B6B')
        location.latitude = request.POST.get('latitude') or None
        location.longitude = request.POST.get('longitude') or None

        if 'image' in request.FILES:
            location.image = request.FILES['image']

        try:
            location.save()
            messages.success(request, f'Location "{location.name}" updated successfully!')
            return redirect('admin_dashboard:locations')
        except Exception as e:
            messages.error(request, f'Error updating location: {str(e)}')

    context = {
        'location': location,
        'title': 'Edit Location'
    }
    return render(request, 'admin/location_form.html', context)


@staff_member_required(login_url='users:login')
def admin_location_delete(request, location_id):
    """Delete a location"""
    location = get_object_or_404(Location, id=location_id)

    if request.method == 'POST':
        # Check if location has bikes
        bike_count = location.bikes.count()
        if bike_count > 0:
            messages.error(request, f'Cannot delete location with {bike_count} bike(s). Please reassign or delete the bikes first.')
            return redirect('admin_dashboard:locations')

        location_name = location.name
        try:
            location.delete()
            messages.success(request, f'Location "{location_name}" deleted successfully!')
            return redirect('admin_dashboard:locations')
        except Exception as e:
            messages.error(request, f'Error deleting location: {str(e)}')

    context = {'location': location}
    return render(request, 'admin/location_confirm_delete.html', context)


@staff_member_required(login_url='users:login')
def admin_location_toggle_status(request, location_id):
    """Toggle location active/inactive status"""
    location = get_object_or_404(Location, id=location_id)

    location.is_active = not location.is_active
    location.save()

    status = "activated" if location.is_active else "deactivated"
    messages.success(request, f'Location "{location.name}" {status} successfully!')

    return redirect('admin_dashboard:locations')
