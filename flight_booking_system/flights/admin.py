from django.contrib import admin
from .models import Flight

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'flight_number', 'airline', 'source', 'destination', 
        'departure_time', 'arrival_time', 'available_seats', 
        'total_seats', 'price'
    ]
    list_filter = ['airline', 'source', 'destination', 'departure_time']
    search_fields = ['flight_number', 'airline', 'source', 'destination']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Flight Information', {
            'fields': ('flight_number', 'airline')
        }),
        ('Route Details', {
            'fields': ('source', 'destination', 'departure_time', 'arrival_time')
        }),
        ('Capacity & Pricing', {
            'fields': ('total_seats', 'available_seats', 'price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
