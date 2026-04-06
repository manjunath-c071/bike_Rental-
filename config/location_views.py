from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from config.models import Location


@require_http_methods(["POST"])
def set_selected_city(request):
    """
    AJAX view to set the selected city in session
    """
    city = request.POST.get('city')

    # Check if the city exists in our Location model
    if Location.objects.filter(name=city, is_active=True).exists():
        request.session['selected_city'] = city
        request.session.modified = True
        return JsonResponse({
            'status': 'success',
            'city': city,
            'message': f'Location changed to {city}'
        })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid city selection'
    }, status=400)


def get_city_data(request):
    """
    View to get all active city data for the modal
    """
    locations = Location.objects.filter(is_active=True).order_by('name')
    cities = []

    for location in locations:
        cities.append({
            'name': location.name,
            'description': location.description or f'Explore {location.name}',
            'icon': location.icon,
            'color': location.color,
            'image_url': location.image.url if location.image else None,
        })

    return JsonResponse({
        'cities': cities,
        'selected_city': request.session.get('selected_city', '')
    })
