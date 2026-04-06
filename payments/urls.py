from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # User payment pages
    path('booking/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('process/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('booking/<int:booking_id>/status/', views.payment_status, name='payment_status'),
    path('booking/<int:booking_id>/retry/', views.retry_payment, name='retry_payment'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('history/', views.payment_history, name='payment_history'),
    
    # Admin payment pages
    path('admin/payments/', views.admin_payment_list, name='admin_payment_list'),
    path('admin/payment/<int:payment_id>/refund/', views.admin_process_refund, name='admin_refund'),
]