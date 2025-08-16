<template>
  <div>
    <div class="hero-section bg-primary text-white text-center py-5 mb-5 rounded">
      <h1 class="display-4">🎵 Welcome to ConcertBook</h1>
      <p class="lead">Discover amazing concerts and book your tickets instantly</p>
    </div>
    
    <div class="row mb-4">
      <div class="col-md-6">
        <h2>Upcoming Concerts</h2>
      </div>
      <div class="col-md-6 text-end">
        <div class="input-group">
          <input 
            type="text" 
            class="form-control" 
            placeholder="Search concerts..."
            v-model="searchQuery"
            @input="filterConcerts"
          >
          <span class="input-group-text">
            <i class="fas fa-search"></i>
          </span>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else class="row">
      <div 
        v-for="concert in filteredConcerts" 
        :key="concert.id" 
        class="col-md-6 col-lg-4 mb-4"
      >
        <div class="card h-100 shadow-sm">
          <img 
            :src="concert.image_url || 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400'" 
            class="card-img-top" 
            :alt="concert.title"
          >
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ concert.title }}</h5>
            <p class="card-text text-muted">
              <i class="fas fa-user me-2"></i>{{ concert.artist }}
            </p>
            <p class="card-text">
              <i class="fas fa-map-marker-alt me-2"></i>{{ concert.venue }}
            </p>
            <p class="card-text">
              <i class="fas fa-calendar me-2"></i>{{ formatDate(concert.date) }}
            </p>
            <p class="card-text">
              <i class="fas fa-ticket-alt me-2"></i>{{ concert.available_tickets }} tickets available
            </p>
            <div class="mt-auto">
              <div class="d-flex justify-content-between align-items-center">
                <span class="h5 text-primary mb-0">${{ concert.price }}</span>
                <router-link 
                  :to="`/concert/${concert.id}`" 
                  class="btn btn-primary"
                >
                  View Details
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="!loading && filteredConcerts.length === 0" class="text-center py-5">
      <h3 class="text-muted">No concerts found</h3>
      <p class="text-muted">Try adjusting your search criteria</p>
    </div>
  </div>
</template>

<script>
import { concertAPI } from '../services/api'

export default {
  name: 'Home',
  data() {
    return {
      concerts: [],
      filteredConcerts: [],
      searchQuery: '',
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.loadConcerts()
  },
  methods: {
    async loadConcerts() {
      try {
        this.loading = true
        const response = await concertAPI.getConcerts()
        this.concerts = response.data
        this.filteredConcerts = this.concerts
      } catch (error) {
        this.error = 'Failed to load concerts. Please try again later.'
        console.error('Error loading concerts:', error)
      } finally {
        this.loading = false
      }
    },
    filterConcerts() {
      if (!this.searchQuery) {
        this.filteredConcerts = this.concerts
      } else {
        const query = this.searchQuery.toLowerCase()
        this.filteredConcerts = this.concerts.filter(concert =>
          concert.title.toLowerCase().includes(query) ||
          concert.artist.toLowerCase().includes(query) ||
          concert.venue.toLowerCase().includes(query)
        )
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
.hero-section {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>
