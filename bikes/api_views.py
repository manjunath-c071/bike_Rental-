"""
API views for admin inline editing
"""

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from bikes.admin_utils import admin_required
from bikes.models import Bike
from config.models import Location
import json


@admin_required
@require_POST
def api_update_bike(request, bike_id):
    """API endpoint to update bike details"""
    try:
        bike = Bike.objects.get(id=bike_id)
        
        # Parse request body
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Update fields
        if 'name' in data:
            bike.name = data['name']
        
        if 'rental_price_hourly' in data:
            bike.rental_price_hourly = float(data['rental_price_hourly'])
        
        if 'rental_price_daily' in data:
            bike.rental_price_daily = float(data['rental_price_daily'])
        
        if 'is_available' in data:
            bike.is_available = data['is_available'] in [True, 'true', '1', 1]
        
        if 'condition' in data:
            bike.condition = data['condition']
        
        if 'description' in data:
            bike.description = data['description']
        
        bike.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Bike "{bike.name}" updated successfully',
            'bike': {
                'id': bike.id,
                'name': bike.name,
                'rental_price_hourly': str(bike.rental_price_hourly),
                'is_available': bike.is_available
            }
        })
    
    except Bike.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Bike not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@admin_required
@require_POST
def api_update_location(request, location_id):
    """API endpoint to update location details"""
    try:
        location = Location.objects.get(id=location_id)
        
        # Parse request body
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Update fields
        if 'name' in data:
            location.name = data['name']
        
        if 'icon' in data:
            location.icon = data['icon']
        
        if 'description' in data:
            location.description = data['description']
        
        if 'color' in data:
            location.color = data['color']
        
        if 'is_active' in data:
            location.is_active = data['is_active'] in [True, 'true', '1', 1]
        
        location.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Location "{location.name}" updated successfully',
            'location': {
                'id': location.id,
                'name': location.name,
                'icon': location.icon,
                'is_active': location.is_active
            }
        })
    
    except Location.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Location not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@admin_required
@require_POST
def api_delete_bike(request, bike_id):
    """API endpoint to delete a bike"""
    try:
        bike = Bike.objects.get(id=bike_id)
        bike_name = bike.name
        bike.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Bike "{bike_name}" has been deleted'
        })
    
    except Bike.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Bike not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@admin_required
@require_POST
def api_delete_location(request, location_id):
    """API endpoint to delete a location"""
    try:
        location = Location.objects.get(id=location_id)
        
        # Check if location has bikes
        if location.bikes.exists():
            return JsonResponse({
                'success': False,
                'error': 'Cannot delete location with bikes. Remove bikes first.'
            }, status=400)
        
        location_name = location.name
        location.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Location "{location_name}" has been deleted'
        })
    
    except Location.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Location not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
