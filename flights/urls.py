"""This script designs URLs for the application."""
from django.urls import path, include
from django.contrib import admin
from . import views

admin.site.site_header = 'Air Starline Admin'

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/staff_login', views.login_staff, name='staff_login'),
    path('view_flights', views.view_flights, name='view_flights'),
    path('self_check_in/<int:pk>', views.self_check_in, name='self_check_in'),
    path('search_by_source', views.search_by_source, name='search_by_source'),
    path(
        'search_by_destination', views.search_by_destination,
        name='search_by_destination'
    ),
    path('staff_home/<int:flight_no>', views.staff_home, name='staff_home'),
    path(
        'view_available_flights/', views.view_available_flights,
        name='view_available_flights'
    ),
    path('book_flight/<int:pk>', views.book_flight, name='book_flight'),
    path(
        'passenger_home/<int:pk>', views.passenger_home, name='passenger_home'
    ),
    path(
        'staff_check_in/<int:pk>', views.staff_check_in, name='staff_check_in'
    ),
    path('view_booking', views.view_booking, name='view_booking'),
    path('pdf_view/<int:flight_no>', views.pdf_view, name="pdf_view"),
    path(
        'pdf_download/<int:flight_no>', views.pdf_download,
        name="pdf_download"
    ),
    path('pdf_invoice/<int:pk>', views.pdf_invoice, name="pdf_invoice"),
    path('dl_invoice/<int:pk>', views.dl_invoice, name="dl_invoice"),

]
