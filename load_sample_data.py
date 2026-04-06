import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from bikes.models import Bike

# Sample bikes data
bikes_data = [
    {
        'name': 'Speed Racer',
        'bike_type': 'Road',
        'brand': 'Trek',
        'model': 'FX 3',
        'year': 2024,
        'city': 'Delhi',
        'rental_price_hourly': 50,
        'rental_price_daily': 300,
        'color': 'Red',
        'description': 'Fast and lightweight road bike perfect for city commuting.',
        'condition': 'New',
        'is_available': True,
    },
    {
        'name': 'Mountain Beast',
        'bike_type': 'MTB',
        'brand': 'Giant',
        'model': 'Talon',
        'year': 2024,
        'city': 'Mumbai',
        'rental_price_hourly': 75,
        'rental_price_daily': 450,
        'color': 'Black',
        'description': 'Rugged mountain bike for off-road adventures.',
        'condition': 'Good',
        'is_available': True,
    },
    {
        'name': 'City Cruiser',
        'bike_type': 'Hybrid',
        'brand': 'Decathlon',
        'model': 'Riverside 100',
        'year': 2023,
        'city': 'Bangalore',
        'rental_price_hourly': 40,
        'rental_price_daily': 250,
        'color': 'Blue',
        'description': 'Comfortable hybrid bike ideal for leisurely city rides.',
        'condition': 'Good',
        'is_available': True,
    },
    {
        'name': 'Electric Glide',
        'bike_type': 'Electric',
        'brand': 'Hero',
        'model': 'Electric Cycle',
        'year': 2024,
        'city': 'Delhi',
        'rental_price_hourly': 100,
        'rental_price_daily': 600,
        'color': 'Green',
        'description': 'Electric bike for effortless long-distance rides.',
        'condition': 'New',
        'is_available': True,
    },
]

# Create bikes if they don't already exist
for bike_data in bikes_data:
    if not Bike.objects.filter(name=bike_data['name']).exists():
        Bike.objects.create(**bike_data)
        print(f"Created: {bike_data['name']}")
    else:
        print(f"Skipped: {bike_data['name']} (already exists)")

print("Sample data loaded successfully!")
