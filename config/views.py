from django.shortcuts import render
from bikes.models import Bike
from config.models import Location


def home(request):
    """
    Home page view with popular bikes
    """
    selected_city = request.session.get('selected_city')
    if selected_city:
        popular_bikes = Bike.objects.filter(location__name=selected_city)
        if not popular_bikes.exists():
            popular_bikes = Bike.objects.all()[:4]
        else:
            popular_bikes = popular_bikes[:4]
    else:
        popular_bikes = Bike.objects.all()[:4]

    # Get active locations for display
    locations = Location.objects.filter(is_active=True).order_by('name')

    context = {
        'popular_bikes': popular_bikes,
        'locations': locations,
    }
    return render(request, 'home.html', context)
