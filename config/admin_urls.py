from django.urls import path
from bikes import admin_views

app_name = 'admin_dashboard'

urlpatterns = [
    # Dashboard
    path('', admin_views.admin_dashboard, name='dashboard'),
    
    # Bike management
    path('bikes/', admin_views.admin_bikes, name='bikes'),
    path('bikes/add/', admin_views.admin_bike_create, name='bike_create'),
    path('bikes/<int:bike_id>/', admin_views.admin_bike_detail, name='bike_detail'),
    path('bikes/<int:bike_id>/edit/', admin_views.admin_bike_edit, name='bike_edit'),
    path('bikes/<int:bike_id>/delete/', admin_views.admin_bike_delete, name='bike_delete'),
    
    # Location management
    path('locations/', admin_views.admin_locations, name='locations'),
    path('locations/add/', admin_views.admin_location_create, name='location_create'),
    path('locations/<int:location_id>/edit/', admin_views.admin_location_edit, name='location_edit'),
    path('locations/<int:location_id>/delete/', admin_views.admin_location_delete, name='location_delete'),
    path('locations/<int:location_id>/toggle/', admin_views.admin_location_toggle_status, name='location_toggle'),
    
    # Booking management
    path('bookings/', admin_views.admin_bookings, name='bookings'),
    path('bookings/<int:booking_id>/', admin_views.admin_booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', admin_views.admin_booking_cancel, name='booking_cancel'),
    
    # User management
    path('users/', admin_views.admin_users, name='users'),
    path('users/<int:user_id>/', admin_views.admin_user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/', admin_views.admin_user_edit, name='user_edit'),
    
    # Reports
    path('reports/', admin_views.admin_reports, name='reports'),
]
