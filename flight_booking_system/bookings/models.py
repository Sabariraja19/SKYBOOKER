from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from flights.models import Flight

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    flight = models.ForeignKey(
        Flight, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    seats_booked = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='confirmed'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_reference = models.CharField(max_length=20, unique=True)
    
    class Meta:
        ordering = ['-booking_date']
        
    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import uuid
            self.booking_reference = str(uuid.uuid4())[:8].upper()
        
        if not self.total_amount:
            self.total_amount = self.flight.price * self.seats_booked
            
        super().save(*args, **kwargs)
    
    def cancel_booking(self):
        if self.status == 'confirmed':
            self.status = 'cancelled'
            # Return seats to flight
            self.flight.available_seats += self.seats_booked
            self.flight.save()
            self.save()
