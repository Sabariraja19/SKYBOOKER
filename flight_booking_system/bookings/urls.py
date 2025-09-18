from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('dashboard/', views.passenger_dashboard, name='passenger_dashboard'),
    path('detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('manage/', views.manage_bookings, name='manage_bookings'),
    path('export/', views.export_bookings_csv, name='export_bookings_csv'),
]