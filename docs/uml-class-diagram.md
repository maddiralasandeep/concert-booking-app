# UML Class Diagram - Concert Booking System

## Backend Models (Django)

```mermaid
classDiagram
    class Concert {
        +int id
        +string title
        +string artist
        +string venue
        +datetime date
        +decimal price
        +int available_tickets
        +text description
        +string image_url
        +datetime created_at
        +datetime updated_at
        +to_dict() dict
        +__str__() string
    }

    class Booking {
        +int id
        +int concert_id
        +string customer_name
        +string customer_email
        +int tickets_booked
        +datetime booking_date
        +decimal total_amount
        +to_dict() dict
        +save() void
        +__str__() string
    }

    Concert ||--o{ Booking : "has many bookings"
```

## Frontend Components (Vue.js)

```mermaid
classDiagram
    class App {
        +string name
        +render() template
    }

    class Home {
        +array concerts
        +array filteredConcerts
        +string searchQuery
        +boolean loading
        +string error
        +loadConcerts() void
        +filterConcerts() void
        +formatDate() string
    }

    class ConcertDetails {
        +object concert
        +boolean loading
        +string error
        +boolean bookingLoading
        +object bookingForm
        +loadConcert() void
        +submitBooking() void
        +formatDate() string
    }

    class BookingConfirmation {
        +object booking
        +boolean loading
        +string error
        +loadBooking() void
        +formatDate() string
    }

    class MyBookings {
        +array bookings
        +boolean loading
        +string error
        +loadBookings() void
        +formatDate() string
    }

    class ApiService {
        +string API_BASE_URL
        +getConcerts() Promise
        +getConcert(id) Promise
        +createConcert(data) Promise
        +createBooking(data) Promise
        +getBookings() Promise
        +getBooking(id) Promise
    }

    App --> Home : routes_to
    App --> ConcertDetails : routes_to
    App --> BookingConfirmation : routes_to
    App --> MyBookings : routes_to
    
    Home --> ApiService : uses
    ConcertDetails --> ApiService : uses
    BookingConfirmation --> ApiService : uses
    MyBookings --> ApiService : uses
```

## API Serializers (Django REST Framework)

```mermaid
classDiagram
    class ConcertSerializer {
        +Meta model
        +array fields
        +array read_only_fields
        +validate() dict
        +create() Concert
        +update() Concert
    }

    class BookingSerializer {
        +Meta model
        +array fields
        +array read_only_fields
        +ConcertSerializer concert
        +int concert_id
        +validate() dict
        +create() Booking
    }

    class BookingCreateSerializer {
        +Meta model
        +array fields
    }

    ConcertSerializer --> Concert : serializes
    BookingSerializer --> Booking : serializes
    BookingSerializer --> ConcertSerializer : includes
    BookingCreateSerializer --> Booking : creates
```

## API Views (Django REST Framework)

```mermaid
classDiagram
    class ConcertListCreateView {
        +QuerySet queryset
        +Serializer serializer_class
        +get() Response
        +post() Response
    }

    class ConcertDetailView {
        +QuerySet queryset
        +Serializer serializer_class
        +get() Response
        +put() Response
        +delete() Response
    }

    class BookingListView {
        +QuerySet queryset
        +Serializer serializer_class
        +get() Response
    }

    class BookingDetailView {
        +QuerySet queryset
        +Serializer serializer_class
        +get() Response
    }

    class CreateBookingView {
        +post() Response
    }

    ConcertListCreateView --> Concert : manages
    ConcertDetailView --> Concert : manages
    BookingListView --> Booking : manages
    BookingDetailView --> Booking : manages
    CreateBookingView --> Booking : creates
```

## Vue.js Router Structure

```mermaid
classDiagram
    class VueRouter {
        +array routes
        +string mode
        +createRouter() Router
    }

    class Route {
        +string path
        +string name
        +Component component
        +boolean props
    }

    VueRouter --> Route : contains
    Route --> Home : maps_to
    Route --> ConcertDetails : maps_to
    Route --> BookingConfirmation : maps_to
    Route --> MyBookings : maps_to
```
