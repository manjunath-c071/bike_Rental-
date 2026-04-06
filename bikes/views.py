from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bike, BIKE_TYPES
from config.models import Location

def bike_list_view(request):
    """Display list of bikes with filters and pagination"""
    bikes = Bike.objects.filter(is_available=True)
    
    # Get filters from request
    city = request.GET.get('city') or request.session.get('selected_city')
    bike_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('search')
    
    # Apply filters
    if city:
        bikes = bikes.filter(location__name=city)
    
    if bike_type:
        bikes = bikes.filter(bike_type=bike_type)
    
    if min_price:
        try:
            bikes = bikes.filter(rental_price_hourly__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            bikes = bikes.filter(rental_price_hourly__lte=float(max_price))
        except ValueError:
            pass
    
    # Search filter
    if search_query:
        bikes = bikes.filter(
            Q(name__icontains=search_query) | 
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    bikes = bikes.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(bikes, 12)  # 12 bikes per page
    page = request.GET.get('page', 1)
    
    try:
        bikes_page = paginator.page(page)
    except PageNotAnInteger:
        bikes_page = paginator.page(1)
    except EmptyPage:
        bikes_page = paginator.page(paginator.num_pages)
    
    from .models import BIKE_TYPES
    # Get active locations for filter
    locations = Location.objects.filter(is_active=True).order_by('name')
    cities = {loc.name: loc.name for loc in locations}  # For backward compatibility
    
    context = {
        'bikes': bikes_page,
        'paginator': paginator,
        'cities': cities,
        'bike_types': BIKE_TYPES,
        'selected_city': city,
        'selected_type': bike_type,
        'min_price': min_price,
        'max_price': max_price,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'bikes/bike_list.html', context)

def bike_detail_view(request, bike_id):
    """Display bike details"""
    bike = get_object_or_404(Bike, id=bike_id)
    context = {'bike': bike}
    return render(request, 'bikes/bike_detail.html', context)
