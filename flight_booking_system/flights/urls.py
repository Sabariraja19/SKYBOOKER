from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/', views.manage_flights, name='manage_flights'),
    path('add/', views.add_flight, name='add_flight'),
    path('edit/<int:flight_id>/', views.edit_flight, name='edit_flight'),
    path('delete/<int:flight_id>/', views.delete_flight, name='delete_flight'),
]