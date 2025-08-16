from django.contrib import admin
from .models import Concert, Booking

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'venue', 'date', 'price', 'available_tickets']
    list_filter = ['date', 'venue', 'artist']
    search_fields = ['title', 'artist', 'venue']
    ordering = ['date']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['concert', 'customer_name', 'customer_email', 'tickets_booked', 'total_amount', 'booking_date']
    list_filter = ['booking_date', 'concert']
    search_fields = ['customer_name', 'customer_email', 'concert__title']
    ordering = ['-booking_date']
