<template>
  <div>
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else-if="booking" class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-success text-white text-center">
            <h3><i class="fas fa-check-circle me-2"></i>Booking Confirmed!</h3>
          </div>
          <div class="card-body">
            <div class="text-center mb-4">
              <h5>Thank you for your booking, {{ booking.customer_name }}!</h5>
              <p class="text-muted">Your tickets have been successfully reserved.</p>
            </div>
            
            <div class="row">
              <div class="col-md-6">
                <h6>Booking Details</h6>
                <table class="table table-borderless">
                  <tr>
                    <td><strong>Booking ID:</strong></td>
                    <td>#{{ booking.id }}</td>
                  </tr>
                  <tr>
                    <td><strong>Customer:</strong></td>
                    <td>{{ booking.customer_name }}</td>
                  </tr>
                  <tr>
                    <td><strong>Email:</strong></td>
                    <td>{{ booking.customer_email }}</td>
                  </tr>
                  <tr>
                    <td><strong>Tickets:</strong></td>
                    <td>{{ booking.tickets_booked }}</td>
                  </tr>
                  <tr>
                    <td><strong>Total Amount:</strong></td>
                    <td class="text-success"><strong>${{ booking.total_amount }}</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Booking Date:</strong></td>
                    <td>{{ formatDate(booking.booking_date) }}</td>
                  </tr>
                </table>
              </div>
              
              <div class="col-md-6" v-if="booking.concert">
                <h6>Concert Details</h6>
                <table class="table table-borderless">
                  <tr>
                    <td><strong>Event:</strong></td>
                    <td>{{ booking.concert.title }}</td>
                  </tr>
                  <tr>
                    <td><strong>Artist:</strong></td>
                    <td>{{ booking.concert.artist }}</td>
                  </tr>
                  <tr>
                    <td><strong>Venue:</strong></td>
                    <td>{{ booking.concert.venue }}</td>
                  </tr>
                  <tr>
                    <td><strong>Date:</strong></td>
                    <td>{{ formatDate(booking.concert.date) }}</td>
                  </tr>
                </table>
              </div>
            </div>
            
            <div class="alert alert-info mt-4">
              <h6><i class="fas fa-info-circle me-2"></i>Important Information</h6>
              <ul class="mb-0">
                <li>Please arrive at the venue at least 30 minutes before the show starts.</li>
                <li>Bring a valid ID for entry verification.</li>
                <li>A confirmation email has been sent to {{ booking.customer_email }}.</li>
                <li>For any changes or cancellations, please contact our support team.</li>
              </ul>
            </div>
            
            <div class="text-center mt-4">
              <router-link to="/" class="btn btn-primary me-3">
                <i class="fas fa-home me-2"></i>Back to Home
              </router-link>
              <router-link to="/my-bookings" class="btn btn-outline-primary">
                <i class="fas fa-list me-2"></i>View All Bookings
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
  name: 'BookingConfirmation',
  props: ['id'],
  data() {
    return {
      booking: null,
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.loadBooking()
  },
  methods: {
    async loadBooking() {
      try {
        this.loading = true
        const response = await bookingAPI.getBooking(this.id)
        this.booking = response.data
      } catch (error) {
        this.error = 'Failed to load booking details. Please try again later.'
        console.error('Error loading booking:', error)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
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
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.table td {
  padding: 0.5rem 0;
}
</style>
