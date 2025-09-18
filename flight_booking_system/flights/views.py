from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime
from .models import Flight
from bookings.models import Booking
from .forms import FlightSearchForm, FlightForm

def home(request):
    form = FlightSearchForm(request.GET or None)
    flights = []
    
    if form.is_valid():
        source = form.cleaned_data.get('source')
        destination = form.cleaned_data.get('destination')
        departure_date = form.cleaned_data.get('departure_date')
        
        flights = Flight.objects.filter(
            source__icontains=source,
            destination__icontains=destination,
            departure_time__date=departure_date,
            available_seats__gt=0
        ).order_by('departure_time')
    
    return render(request, 'flights/home.html', {
        'form': form,
        'flights': flights
    })

def flight_list(request):
    flights = Flight.objects.filter(
        departure_time__gte=timezone.now(),
        available_seats__gt=0
    ).order_by('departure_time')
    
    # Filter by search parameters
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    date = request.GET.get('date')
    
    if source:
        flights = flights.filter(source__icontains=source)
    if destination:
        flights = flights.filter(destination__icontains=destination)
    if date:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            flights = flights.filter(departure_time__date=date_obj)
        except ValueError:
            pass
    
    return render(request, 'flights/flight_list.html', {'flights': flights})

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    return render(request, 'flights/flight_detail.html', {'flight': flight})

@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Dashboard statistics
    total_flights = Flight.objects.count()
    total_bookings = Booking.objects.filter(status='confirmed').count()
    total_revenue = Booking.objects.filter(status='confirmed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    recent_bookings = Booking.objects.filter(status='confirmed').order_by('-booking_date')[:10]
    upcoming_flights = Flight.objects.filter(
        departure_time__gte=timezone.now()
    ).order_by('departure_time')[:10]
    
    context = {
        'total_flights': total_flights,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'upcoming_flights': upcoming_flights,
    }
    
    return render(request, 'flights/admin_dashboard.html', context)

@login_required
def manage_flights(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    flights = Flight.objects.all().order_by('-created_at')
    return render(request, 'flights/manage_flights.html', {'flights': flights})

@login_required
def add_flight(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save()
            messages.success(request, f'Flight {flight.flight_number} added successfully!')
            return redirect('manage_flights')
    else:
        form = FlightForm()
    
    return render(request, 'flights/add_flight.html', {'form': form})

@login_required
def edit_flight(request, flight_id):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    flight = get_object_or_404(Flight, id=flight_id)
    
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, f'Flight {flight.flight_number} updated successfully!')
            return redirect('manage_flights')
    else:
        form = FlightForm(instance=flight)
    
    return render(request, 'flights/edit_flight.html', {'form': form, 'flight': flight})

@login_required
def delete_flight(request, flight_id):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    flight = get_object_or_404(Flight, id=flight_id)
    
    if request.method == 'POST':
        flight_number = flight.flight_number
        flight.delete()
        messages.success(request, f'Flight {flight_number} deleted successfully!')
        return redirect('manage_flights')
    
    return render(request, 'flights/delete_flight.html', {'flight': flight})
