from django.core.management.base import BaseCommand
from config.models import Location
from bikes.models import Bike


class Command(BaseCommand):
    help = 'Populate Location objects and migrate existing bikes to use them'

    def handle(self, *args, **options):
        # Define location data
        locations_data = {
            'Delhi': {
                'description': 'Capital city of India',
                'icon': '🏛️',
                'color': '#FF6B6B',
                'latitude': 28.7041,
                'longitude': 77.1025,
            },
            'Mumbai': {
                'description': 'Financial capital of India',
                'icon': '🌆',
                'color': '#4ECDC4',
                'latitude': 19.0760,
                'longitude': 72.8777,
            },
            'Bangalore': {
                'description': 'Silicon Valley of India',
                'icon': '🏢',
                'color': '#45B7D1',
                'latitude': 12.9716,
                'longitude': 77.5946,
            },
        }

        # Create Location objects
        locations = {}
        for city_name, data in locations_data.items():
            location, created = Location.objects.get_or_create(
                name=city_name,
                defaults={
                    'description': data['description'],
                    'icon': data['icon'],
                    'color': data['color'],
                    'latitude': data['latitude'],
                    'longitude': data['longitude'],
                    'is_active': True,
                }
            )
            locations[city_name] = location
            if created:
                self.stdout.write(f"Created location: {city_name}")
            else:
                self.stdout.write(f"Location already exists: {city_name}")

        # Update existing bikes to reference locations based on their names
        # (since city field was removed, we use bike names to determine location)
        bike_location_mapping = {
            'Speed Racer': 'Delhi',
            'Mountain Beast': 'Mumbai',
            'City Cruiser': 'Bangalore',
            'Electric Glide': 'Delhi',
        }
        
        bikes_updated = 0
        for bike in Bike.objects.all():
            if bike.location is None and bike.name in bike_location_mapping:
                location_name = bike_location_mapping[bike.name]
                if location_name in locations:
                    bike.location = locations[location_name]
                    bike.save()
                    bikes_updated += 1
                    self.stdout.write(f"Updated bike '{bike.name}' to location '{location_name}'")
            elif bike.location is None:
                # Assign a default location for any unmapped bikes
                default_location = locations.get('Delhi')  # Default to Delhi
                if default_location:
                    bike.location = default_location
                    bike.save()
                    bikes_updated += 1
                    self.stdout.write(f"Updated bike '{bike.name}' to default location 'Delhi'")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(locations)} locations and updated {bikes_updated} bikes'
            )
        )