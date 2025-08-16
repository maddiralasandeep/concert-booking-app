from django.urls import path
from . import views

urlpatterns = [
    path('concerts/', views.ConcertListCreateView.as_view(), name='concert-list-create'),
    path('concerts/<int:pk>/', views.ConcertDetailView.as_view(), name='concert-detail'),
    path('bookings/', views.create_booking, name='booking-create'),
    path('bookings/list/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
]
