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
    
    <div v-else-if="concert" class="row">
      <div class="col-md-6">
        <img 
          :src="concert.image_url || 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600'" 
          class="img-fluid rounded" 
          :alt="concert.title"
        >
      </div>
      
      <div class="col-md-6">
        <h1>{{ concert.title }}</h1>
        <h3 class="text-muted mb-3">{{ concert.artist }}</h3>
        
        <div class="mb-3">
          <h5><i class="fas fa-map-marker-alt me-2"></i>Venue</h5>
          <p>{{ concert.venue }}</p>
        </div>
        
        <div class="mb-3">
          <h5><i class="fas fa-calendar me-2"></i>Date & Time</h5>
          <p>{{ formatDate(concert.date) }}</p>
        </div>
        
        <div class="mb-3">
          <h5><i class="fas fa-ticket-alt me-2"></i>Availability</h5>
          <p>{{ concert.available_tickets }} tickets remaining</p>
        </div>
        
        <div class="mb-4">
          <h5><i class="fas fa-dollar-sign me-2"></i>Price</h5>
          <h3 class="text-primary">${{ concert.price }}</h3>
        </div>
        
        <div v-if="concert.description" class="mb-4">
          <h5>Description</h5>
          <p>{{ concert.description }}</p>
        </div>
        
        <!-- Booking Form -->
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Book Tickets</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="submitBooking">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="customerName" class="form-label">Full Name</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="customerName"
                    v-model="bookingForm.customer_name"
                    required
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label for="customerEmail" class="form-label">Email</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    id="customerEmail"
                    v-model="bookingForm.customer_email"
                    required
                  >
                </div>
              </div>
              
              <div class="mb-3">
                <label for="ticketsBooked" class="form-label">Number of Tickets</label>
                <select 
                  class="form-select" 
                  id="ticketsBooked"
                  v-model="bookingForm.tickets_booked"
                  required
                >
                  <option value="">Select number of tickets</option>
                  <option 
                    v-for="n in Math.min(concert.available_tickets, 10)" 
                    :key="n" 
                    :value="n"
                  >
                    {{ n }} ticket{{ n > 1 ? 's' : '' }}
                  </option>
                </select>
              </div>
              
              <div v-if="bookingForm.tickets_booked" class="mb-3">
                <h6>Total Amount: ${{ (concert.price * bookingForm.tickets_booked).toFixed(2) }}</h6>
              </div>
              
              <button 
                type="submit" 
                class="btn btn-primary btn-lg w-100"
                :disabled="bookingLoading || concert.available_tickets === 0"
              >
                <span v-if="bookingLoading" class="spinner-border spinner-border-sm me-2"></span>
                {{ concert.available_tickets === 0 ? 'Sold Out' : 'Book Now' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { concertAPI, bookingAPI } from '../services/api'

export default {
  name: 'ConcertDetails',
  props: ['id'],
  data() {
    return {
      concert: null,
      loading: true,
      error: null,
      bookingLoading: false,
      bookingForm: {
        customer_name: '',
        customer_email: '',
        tickets_booked: '',
        concert_id: null
      }
    }
  },
  async mounted() {
    await this.loadConcert()
  },
  methods: {
    async loadConcert() {
      try {
        this.loading = true
        const response = await concertAPI.getConcert(this.id)
        this.concert = response.data
        this.bookingForm.concert_id = this.concert.id
      } catch (error) {
        this.error = 'Failed to load concert details. Please try again later.'
        console.error('Error loading concert:', error)
      } finally {
        this.loading = false
      }
    },
    async submitBooking() {
      try {
        this.bookingLoading = true
        const response = await bookingAPI.createBooking(this.bookingForm)
        
        // Redirect to booking confirmation
        this.$router.push(`/booking-confirmation/${response.data.id}`)
      } catch (error) {
        let errorMessage = 'Failed to create booking. Please try again.'
        
        if (error.response && error.response.data) {
          if (typeof error.response.data === 'string') {
            errorMessage = error.response.data
          } else if (error.response.data.error) {
            errorMessage = error.response.data.error
          } else if (error.response.data.non_field_errors) {
            errorMessage = error.response.data.non_field_errors[0]
          }
        }
        
        alert(errorMessage)
        console.error('Error creating booking:', error)
      } finally {
        this.bookingLoading = false
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

.img-fluid {
  max-height: 400px;
  object-fit: cover;
  width: 100%;
}
</style>
