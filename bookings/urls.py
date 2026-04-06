from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list_view, name='booking_list'),
    path('create/', views.booking_create_view, name='booking_create'),
    path('<int:booking_id>/confirmation/', views.booking_confirmation_view, name='booking_confirmation'),
    path('<int:booking_id>/', views.booking_detail_view, name='booking_detail'),
    path('<int:booking_id>/cancel/', views.booking_cancel_view, name='booking_cancel'),
    path('api/calculate-price/', views.calculate_price_view, name='calculate_price'),
]
