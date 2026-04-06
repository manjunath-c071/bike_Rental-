from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime
from decimal import Decimal
from .models import Booking
from .forms import BookingForm
from bikes.models import Bike

@login_required(login_url='users:login')
def booking_list_view(request):
    """View user's booking history"""
    bookings = request.user.bookings.all().order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    
    context = {
        'bookings': bookings,
        'status_filter': status,
    }
    return render(request, 'bookings/booking_list.html', context)

@login_required(login_url='users:login')
def booking_create_view(request):
    """Create a new booking - Status: Pending (payment required)"""
    bike_id = request.GET.get('bike_id')
    bike = get_object_or_404(Bike, id=bike_id) if bike_id else None
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.bike = bike
                # IMPORTANT: Booking starts as 'pending' - will be confirmed after payment
                booking.status = 'pending'
                booking.save()
                
                messages.success(request, 'Booking created! Proceeding to payment...')
                # Redirect to payment page instead of confirmation
                return redirect('payments:payment_page', booking_id=booking.id)
            except Exception as e:
                messages.error(request, f'Error creating booking: {str(e)}')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BookingForm()
    
    context = {
        'bike': bike,
        'form': form,
        'is_user': True,  # Pass to template for UX
    }
    return render(request, 'bookings/booking_create.html', context)

@login_required(login_url='users:login')
def booking_confirmation_view(request, booking_id):
    """Show booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {'booking': booking}
    return render(request, 'bookings/booking_confirmation.html', context)

@login_required(login_url='users:login')
def booking_detail_view(request, booking_id):
    """View booking details"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    context = {'booking': booking}
    return render(request, 'bookings/booking_detail.html', context)

@login_required(login_url='users:login')
def booking_cancel_view(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    
    return redirect('bookings:booking_list')

@require_POST
def calculate_price_view(request):
    """AJAX endpoint to calculate booking price"""
    try:
        bike_id = request.POST.get('bike_id')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        insurance = request.POST.get('insurance') == 'true'
        
        bike = get_object_or_404(Bike, id=bike_id)
        
        # Parse dates
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
        
        # Calculate duration
        duration = Decimal(str((end_date - start_date).total_seconds() / 3600))
        
        if duration <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'End date must be after start date'
            }, status=400)
        
        # Calculate cost
        hourly_rate = bike.rental_price_hourly
        rental_cost = hourly_rate * duration
        insurance_amount = rental_cost * Decimal('0.05') if insurance else 0
        total_cost = rental_cost + insurance_amount
        
        return JsonResponse({
            'status': 'success',
            'duration': round(duration, 1),
            'hourly_rate': float(hourly_rate),
            'rental_cost': round(rental_cost, 2),
            'insurance_amount': round(insurance_amount, 2),
            'total_cost': round(total_cost, 2),
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
