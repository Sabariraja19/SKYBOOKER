from django import forms
from django.utils import timezone
from .models import Flight

class FlightSearchForm(forms.Form):
    source = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark border-secondary text-white',
            'placeholder': 'From (e.g., New York)',
            'style': 'color: white !important;'
        })
    )
    destination = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark border-secondary text-white',
            'placeholder': 'To (e.g., Los Angeles)',
            'style': 'color: white !important;'
        })
    )
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control bg-dark border-secondary text-white',
            'type': 'date',
            'min': timezone.now().date(),
            'style': 'color: white !important;'
        })
    )

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_number', 'airline', 'source', 'destination',
            'departure_time', 'arrival_time', 'total_seats', 'available_seats', 'price'
        ]
        widgets = {
            'flight_number': forms.TextInput(attrs={'class': 'form-control'}),
            'airline': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'arrival_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        departure_time = cleaned_data.get('departure_time')
        arrival_time = cleaned_data.get('arrival_time')
        total_seats = cleaned_data.get('total_seats')
        available_seats = cleaned_data.get('available_seats')
        
        if departure_time and arrival_time:
            if departure_time >= arrival_time:
                raise forms.ValidationError('Arrival time must be after departure time.')
        
        if total_seats and available_seats:
            if available_seats > total_seats:
                raise forms.ValidationError('Available seats cannot exceed total seats.')
        
        return cleaned_data