from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
import csv
from .models import Booking
from flights.models import Flight
from .forms import BookingForm

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    
    if not flight.is_available():
        messages.error(request, 'This flight is fully booked.')
        return redirect('flight_detail', flight_id=flight_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, flight=flight)
        if form.is_valid():
            seats_requested = form.cleaned_data['seats_booked']
            
            # Check if enough seats are available
            if seats_requested > flight.available_seats:
                messages.error(request, f'Only {flight.available_seats} seats available.')
                return render(request, 'bookings/book_flight.html', {
                    'form': form,
                    'flight': flight
                })
            
            # Create booking with transaction to ensure data consistency
            with transaction.atomic():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.flight = flight
                booking.total_amount = flight.price * seats_requested
                booking.save()
                
                # Update available seats
                flight.available_seats -= seats_requested
                flight.save()
            
            messages.success(request, f'Booking confirmed! Reference: {booking.booking_reference}')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm(flight=flight)
    
    return render(request, 'bookings/book_flight.html', {
        'form': form,
        'flight': flight
    })

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})

@login_required
def passenger_dashboard(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/passenger_dashboard.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user can view this booking
    if not request.user.is_admin() and booking.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('passenger_dashboard')
    
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user can cancel this booking
    if not request.user.is_admin() and booking.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('passenger_dashboard')
    
    if booking.status != 'confirmed':
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', booking_id=booking_id)
    
    if request.method == 'POST':
        with transaction.atomic():
            booking.cancel_booking()
        
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('passenger_dashboard' if not request.user.is_admin() else 'admin_dashboard')
    
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})

@login_required
def manage_bookings(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    bookings = Booking.objects.all().order_by('-booking_date')
    return render(request, 'bookings/manage_bookings.html', {'bookings': bookings})

@login_required
def export_bookings_csv(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bookings.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Booking Reference', 'User', 'Flight Number', 'Airline', 
        'Source', 'Destination', 'Departure Time', 'Seats Booked', 
        'Total Amount', 'Status', 'Booking Date'
    ])
    
    bookings = Booking.objects.select_related('user', 'flight').all()
    for booking in bookings:
        writer.writerow([
            booking.booking_reference,
            booking.user.username,
            booking.flight.flight_number,
            booking.flight.airline,
            booking.flight.source,
            booking.flight.destination,
            booking.flight.departure_time,
            booking.seats_booked,
            booking.total_amount,
            booking.status,
            booking.booking_date,
        ])
    
    return response
