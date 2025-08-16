<template>
  <div>
    <h2 class="mb-4">My Bookings</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="bookings.length === 0" class="text-center py-5">
      <h4 class="text-muted">No bookings found</h4>
      <p class="text-muted">You haven't made any bookings yet.</p>
      <router-link to="/" class="btn btn-primary">
        <i class="fas fa-music me-2"></i>Browse Concerts
      </router-link>
    </div>
    
    <div v-else>
      <div class="row">
        <div 
          v-for="booking in bookings" 
          :key="booking.id" 
          class="col-md-6 col-lg-4 mb-4"
        >
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <span class="badge bg-success">Confirmed</span>
              <small class="text-muted">Booking #{{ booking.id }}</small>
            </div>
            
            <div class="card-body">
              <h5 class="card-title">{{ booking.concert.title }}</h5>
              <p class="card-text text-muted">
                <i class="fas fa-user me-2"></i>{{ booking.concert.artist }}
              </p>
              <p class="card-text">
                <i class="fas fa-map-marker-alt me-2"></i>{{ booking.concert.venue }}
              </p>
              <p class="card-text">
                <i class="fas fa-calendar me-2"></i>{{ formatDate(booking.concert.date) }}
              </p>
              
              <hr>
              
              <div class="row">
                <div class="col-6">
                  <small class="text-muted">Tickets</small>
                  <p class="mb-1"><strong>{{ booking.tickets_booked }}</strong></p>
                </div>
                <div class="col-6">
                  <small class="text-muted">Total Paid</small>
                  <p class="mb-1 text-success"><strong>${{ booking.total_amount }}</strong></p>
                </div>
              </div>
              
              <small class="text-muted">
                Booked on {{ formatDate(booking.booking_date) }}
              </small>
            </div>
            
            <div class="card-footer">
              <router-link 
                :to="`/booking-confirmation/${booking.id}`" 
                class="btn btn-outline-primary btn-sm w-100"
              >
                View Details
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { bookingAPI } from '../services/api'

export default {
  name: 'MyBookings',
  data() {
    return {
      bookings: [],
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.loadBookings()
  },
  methods: {
    async loadBookings() {
      try {
        this.loading = true
        const response = await bookingAPI.getBookings()
        this.bookings = response.data
      } catch (error) {
        this.error = 'Failed to load bookings. Please try again later.'
        console.error('Error loading bookings:', error)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}
</style>
