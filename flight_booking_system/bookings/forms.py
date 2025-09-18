from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats_booked']
        widgets = {
            'seats_booked': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of seats'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)
        
        if self.flight:
            self.fields['seats_booked'].widget.attrs['max'] = str(self.flight.available_seats)
            self.fields['seats_booked'].help_text = f'Available seats: {self.flight.available_seats}'
    
    def clean_seats_booked(self):
        seats_booked = self.cleaned_data['seats_booked']
        
        if seats_booked <= 0:
            raise forms.ValidationError('Number of seats must be greater than 0.')
        
        if self.flight and seats_booked > self.flight.available_seats:
            raise forms.ValidationError(f'Only {self.flight.available_seats} seats available.')
        
        return seats_booked