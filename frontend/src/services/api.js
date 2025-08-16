import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const concertAPI = {
  // Get all concerts
  getConcerts() {
    return api.get('/concerts')
  },
  
  // Get a specific concert by ID
  getConcert(id) {
    return api.get(`/concerts/${id}`)
  },
  
  // Create a new concert (admin functionality)
  createConcert(concertData) {
    return api.post('/concerts', concertData)
  }
}

export const bookingAPI = {
  // Create a new booking
  createBooking(bookingData) {
    return api.post('/bookings/', bookingData)
  },
  
  // Get all bookings
  getBookings() {
    return api.get('/bookings/list/')
  },
  
  // Get a specific booking by ID
  getBooking(id) {
    return api.get(`/bookings/${id}/`)
  }
}

export default api
