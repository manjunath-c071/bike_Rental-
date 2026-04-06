"""
URL configuration for RideNova project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config.views import home
from config.location_views import set_selected_city, get_city_data
from bikes.api_views import (
    api_update_bike, api_delete_bike,
    api_update_location, api_delete_location
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('config.admin_urls')),
    path('', home, name='home'),
    path('api/set-city/', set_selected_city, name='set_city'),
    path('api/get-cities/', get_city_data, name='get_cities'),
    
    # API endpoints for inline editing
    path('api/admin/bike/<int:bike_id>/update/', api_update_bike, name='api_update_bike'),
    path('api/admin/bike/<int:bike_id>/delete/', api_delete_bike, name='api_delete_bike'),
    path('api/admin/location/<int:location_id>/update/', api_update_location, name='api_update_location'),
    path('api/admin/location/<int:location_id>/delete/', api_delete_location, name='api_delete_location'),
    
    path('users/', include('users.urls')),
    path('bikes/', include('bikes.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
