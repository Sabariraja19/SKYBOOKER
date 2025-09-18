from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_seats = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    total_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['departure_time']
        
    def __str__(self):
        return f"{self.flight_number} - {self.source} to {self.destination}"
    
    def is_available(self):
        return self.available_seats > 0
    
    def get_booked_seats(self):
        return self.total_seats - self.available_seats
    
    def get_duration(self):
        return self.arrival_time - self.departure_time
