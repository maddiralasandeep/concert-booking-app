from django.db import models
from django.utils import timezone

class Concert(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    venue = models.CharField(max_length=200)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_tickets = models.IntegerField()
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Booking(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    tickets_booked = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"Booking for {self.concert.title} by {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.concert.price * self.tickets_booked
        super().save(*args, **kwargs)
