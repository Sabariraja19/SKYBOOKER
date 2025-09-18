from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_reference', 'user', 'flight', 'seats_booked', 
        'total_amount', 'status', 'booking_date'
    ]
    list_filter = ['status', 'booking_date', 'flight__airline']
    search_fields = [
        'booking_reference', 'user__username', 'user__email',
        'flight__flight_number', 'flight__airline'
    ]
    readonly_fields = ['booking_reference', 'total_amount', 'booking_date']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_reference', 'user', 'flight')
        }),
        ('Booking Details', {
            'fields': ('seats_booked', 'total_amount', 'status')
        }),
        ('Timestamps', {
            'fields': ('booking_date',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['user', 'flight', 'seats_booked']
        return self.readonly_fields
