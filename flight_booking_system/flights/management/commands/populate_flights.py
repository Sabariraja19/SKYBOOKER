from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from flights.models import Flight

class Command(BaseCommand):
    help = 'Populate the database with sample flight data'

    def handle(self, *args, **options):
        # Clear existing flights
        Flight.objects.all().delete()
        
        # Sample flight data
        flights_data = [
            {
                'flight_number': 'AA101',
                'airline': 'American Airlines',
                'source': 'New York',
                'destination': 'Los Angeles',
                'departure_time': timezone.now() + timedelta(days=1, hours=8),
                'arrival_time': timezone.now() + timedelta(days=1, hours=14),
                'total_seats': 180,
                'available_seats': 150,
                'price': 299.99,
            },
            {
                'flight_number': 'DL205',
                'airline': 'Delta Airlines',
                'source': 'Chicago',
                'destination': 'Miami',
                'departure_time': timezone.now() + timedelta(days=2, hours=10),
                'arrival_time': timezone.now() + timedelta(days=2, hours=15),
                'total_seats': 160,
                'available_seats': 120,
                'price': 249.99,
            },
            {
                'flight_number': 'UA308',
                'airline': 'United Airlines',
                'source': 'San Francisco',
                'destination': 'Seattle',
                'departure_time': timezone.now() + timedelta(days=1, hours=12),
                'arrival_time': timezone.now() + timedelta(days=1, hours=14, minutes=30),
                'total_seats': 140,
                'available_seats': 100,
                'price': 189.99,
            },
            {
                'flight_number': 'BA401',
                'airline': 'British Airways',
                'source': 'New York',
                'destination': 'London',
                'departure_time': timezone.now() + timedelta(days=3, hours=20),
                'arrival_time': timezone.now() + timedelta(days=4, hours=8),
                'total_seats': 250,
                'available_seats': 200,
                'price': 599.99,
            },
            {
                'flight_number': 'LH502',
                'airline': 'Lufthansa',
                'source': 'Chicago',
                'destination': 'Frankfurt',
                'departure_time': timezone.now() + timedelta(days=4, hours=16),
                'arrival_time': timezone.now() + timedelta(days=5, hours=8),
                'total_seats': 300,
                'available_seats': 250,
                'price': 649.99,
            },
            {
                'flight_number': 'JL603',
                'airline': 'Japan Airlines',
                'source': 'Los Angeles',
                'destination': 'Tokyo',
                'departure_time': timezone.now() + timedelta(days=5, hours=14),
                'arrival_time': timezone.now() + timedelta(days=6, hours=18),
                'total_seats': 280,
                'available_seats': 220,
                'price': 799.99,
            },
            {
                'flight_number': 'AF704',
                'airline': 'Air France',
                'source': 'Miami',
                'destination': 'Paris',
                'departure_time': timezone.now() + timedelta(days=6, hours=22),
                'arrival_time': timezone.now() + timedelta(days=7, hours=14),
                'total_seats': 220,
                'available_seats': 180,
                'price': 579.99,
            },
            {
                'flight_number': 'EK805',
                'airline': 'Emirates',
                'source': 'New York',
                'destination': 'Dubai',
                'departure_time': timezone.now() + timedelta(days=7, hours=23),
                'arrival_time': timezone.now() + timedelta(days=8, hours=19),
                'total_seats': 350,
                'available_seats': 300,
                'price': 899.99,
            },
            {
                'flight_number': 'WN906',
                'airline': 'Southwest Airlines',
                'source': 'Denver',
                'destination': 'Phoenix',
                'departure_time': timezone.now() + timedelta(days=2, hours=15),
                'arrival_time': timezone.now() + timedelta(days=2, hours=17),
                'total_seats': 150,
                'available_seats': 130,
                'price': 129.99,
            },
            {
                'flight_number': 'AC107',
                'airline': 'Air Canada',
                'source': 'Seattle',
                'destination': 'Vancouver',
                'departure_time': timezone.now() + timedelta(days=3, hours=9),
                'arrival_time': timezone.now() + timedelta(days=3, hours=10, minutes=30),
                'total_seats': 120,
                'available_seats': 90,
                'price': 159.99,
            }
        ]
        
        # Create flight objects
        created_flights = []
        for flight_data in flights_data:
            flight = Flight.objects.create(**flight_data)
            created_flights.append(flight)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_flights)} sample flights'
            )
        )
        
        # Display created flights
        for flight in created_flights:
            self.stdout.write(f'  - {flight.flight_number}: {flight.source} → {flight.destination} (${flight.price})')