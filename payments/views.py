from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
from django.db import transaction
from bookings.models import Booking
from .models import Payment
import json


@login_required(login_url='users:login')
def payment_page(request, booking_id):
    """Display payment page for a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if payment already exists
    try:
        payment = booking.payment
        if payment.status == 'completed':
            messages.info(request, 'This booking is already paid.')
            return redirect('bookings:booking_detail', booking_id=booking_id)
    except Payment.DoesNotExist:
        payment = None
    
    # Calculate total amount including insurance/extras if any
    amount = booking.total_cost
    
    context = {
        'booking': booking,
        'payment': payment,
        'amount': amount,
        'payment_methods': Payment._meta.get_field('payment_method').choices,
    }
    return render(request, 'payments/payment_page.html', context)


@login_required(login_url='users:login')
@require_http_methods(['POST'])
@transaction.atomic
def process_payment(request, booking_id):
    """Process payment for a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Parse request data
    try:
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
    except json.JSONDecodeError:
        data = request.POST
    
    payment_method = data.get('payment_method', 'card')
    total_amount = float(data.get('amount', booking.total_cost))
    
    # Validate amount
    if total_amount != float(booking.total_cost):
        return JsonResponse({
            'success': False,
            'error': 'Amount mismatch. Please refresh and try again.'
        }, status=400)
    
    # Check if payment already exists
    try:
        payment = booking.payment
        if payment.status == 'completed':
            return JsonResponse({
                'success': False,
                'error': 'This booking is already paid.'
            }, status=400)
    except Payment.DoesNotExist:
        # Create new payment record
        payment = Payment.objects.create(
            booking=booking,
            user=request.user,
            amount=total_amount,
            payment_method=payment_method,
            status='pending',
            description=f'Payment for bike booking #{booking.id}'
        )
    
    # Here you would integrate with actual payment gateway
    # For demo purposes, we'll simulate payment processing
    
    try:
        # Simulate payment processing
        payment.status = 'processing'
        payment.save()
        
        # Simulate successful payment (in production, this would call payment gateway API)
        success = True  # This should be based on actual payment gateway response
        
        if success:
            # Mark payment as completed
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.gateway_reference = f'SIM-{payment.transaction_id}'
            payment.save()
            
            # Update booking status
            booking.status = 'confirmed'
            booking.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Payment successful!',
                'payment_id': payment.id,
                'transaction_id': payment.transaction_id,
                'redirect_url': f'/bookings/{booking.id}/'
            })
        else:
            payment.status = 'failed'
            payment.save()
            return JsonResponse({
                'success': False,
                'error': 'Payment failed. Please try again.'
            }, status=400)
    
    except Exception as e:
        payment.status = 'failed'
        payment.notes = str(e)
        payment.save()
        
        return JsonResponse({
            'success': False,
            'error': f'Payment processing error: {str(e)}'
        }, status=500)


@login_required(login_url='users:login')
@require_POST
def retry_payment(request, booking_id):
    """Retry payment for a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    return redirect('payments:payment_page', booking_id=booking_id)


@login_required(login_url='users:login')
def payment_success(request, booking_id):
    """Display payment success page after confirmed payment"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Verify booking is confirmed
    if booking.status != 'confirmed':
        messages.warning(request, 'This booking is not confirmed yet.')
        return redirect('payments:payment_page', booking_id=booking_id)
    
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found for this booking.')
        return redirect('bookings:booking_detail', booking_id=booking_id)
    
    context = {
        'booking': booking,
        'payment': payment,
    }
    return render(request, 'payments/payment_success.html', context)


@login_required(login_url='users:login')
def payment_status(request, booking_id):
    """Check payment status via AJAX"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    try:
        payment = booking.payment
        return JsonResponse({
            'status': payment.status,
            'amount': str(payment.amount),
            'transaction_id': payment.transaction_id,
            'completed': payment.is_successful,
        })
    except Payment.DoesNotExist:
        return JsonResponse({
            'status': 'none',
            'error': 'No payment found for this booking'
        }, status=404)


@login_required(login_url='users:login')
def payment_history(request):
    """View user's payment history"""
    payments = Payment.objects.filter(user=request.user).select_related('booking').order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        payments = payments.filter(status=status)
    
    context = {
        'payments': payments,
        'status_filter': status,
        'payment_statuses': Payment._meta.get_field('status').choices,
    }
    return render(request, 'payments/payment_history.html', context)


# ADMIN PAYMENT VIEWS

from bikes.admin_utils import admin_required


@admin_required
def admin_payment_list(request):
    """Admin view for all payments"""
    payments = Payment.objects.all().select_related('booking', 'user').order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        payments = payments.filter(status=status)
    
    # Filter by user
    user_id = request.GET.get('user')
    if user_id:
        payments = payments.filter(user_id=user_id)
    
    # Search by transaction ID
    search = request.GET.get('search')
    if search:
        payments = payments.filter(transaction_id__icontains=search)
    
    from django.core.paginator import Paginator
    paginator = Paginator(payments, 20)
    page = request.GET.get('page', 1)
    payments_page = paginator.get_page(page)
    
    context = {
        'payments': payments_page,
        'status_filter': status,
        'user_filter': user_id,
        'search_query': search,
        'payment_statuses': Payment._meta.get_field('status').choices,
    }
    return render(request, 'admin/payments.html', context)


@admin_required
@require_http_methods(['POST'])
def admin_process_refund(request, payment_id):
    """Admin can process refund"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if payment.status == 'completed':
        payment.status = 'refunded'
        payment.notes = request.POST.get('reason', 'Refund requested')
        payment.save()
        
        # Update booking status
        payment.booking.status = 'cancelled'
        payment.booking.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Payment {payment.transaction_id} refunded successfully'
            })
        else:
            messages.success(request, f'Payment refunded successfully')
            return redirect('admin:payment_list')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Can only refund completed payments'
        }, status=400)
    else:
        messages.error(request, 'Can only refund completed payments')
        return redirect('admin:payment_list')