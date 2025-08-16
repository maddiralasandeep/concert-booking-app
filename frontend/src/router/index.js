import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ConcertDetails from '../views/ConcertDetails.vue'
import BookingConfirmation from '../views/BookingConfirmation.vue'
import MyBookings from '../views/MyBookings.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/concert/:id',
    name: 'ConcertDetails',
    component: ConcertDetails,
    props: true
  },
  {
    path: '/booking-confirmation/:id',
    name: 'BookingConfirmation',
    component: BookingConfirmation,
    props: true
  },
  {
    path: '/my-bookings',
    name: 'MyBookings',
    component: MyBookings
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
