# System Architecture Diagram - Concert Booking App

## High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
        Mobile[Mobile Browser]
    end

    subgraph "Frontend Layer - Vue.js SPA"
        VueApp[Vue.js Application]
        Router[Vue Router]
        Components[Vue Components]
        ApiService[API Service Layer]
    end

    subgraph "Backend Layer - Django"
        DjangoApp[Django Application]
        RestAPI[Django REST Framework]
        Models[Django Models]
        Admin[Django Admin]
    end

    subgraph "Database Layer"
        SQLite[(SQLite Database)]
    end

    subgraph "External Services"
        Unsplash[Unsplash Images API]
        Bootstrap[Bootstrap CDN]
        FontAwesome[Font Awesome CDN]
    end

    Browser --> VueApp
    Mobile --> VueApp
    VueApp --> Router
    Router --> Components
    Components --> ApiService
    ApiService -->|HTTP/REST API| RestAPI
    RestAPI --> DjangoApp
    DjangoApp --> Models
    Models --> SQLite
    Admin --> Models
    Components --> Bootstrap
    Components --> FontAwesome
    Components --> Unsplash
```

## Detailed Component Architecture

```mermaid
graph LR
    subgraph "Frontend Components"
        App[App.vue]
        Home[Home.vue]
        Details[ConcertDetails.vue]
        Booking[BookingConfirmation.vue]
        MyBookings[MyBookings.vue]
    end

    subgraph "Frontend Services"
        API[api.js]
        Router[router/index.js]
    end

    subgraph "Backend Views"
        ConcertList[ConcertListCreateView]
        ConcertDetail[ConcertDetailView]
        BookingList[BookingListView]
        BookingDetail[BookingDetailView]
        CreateBooking[create_booking]
    end

    subgraph "Backend Models"
        Concert[Concert Model]
        BookingModel[Booking Model]
    end

    App --> Home
    App --> Details
    App --> Booking
    App --> MyBookings
    
    Home --> API
    Details --> API
    Booking --> API
    MyBookings --> API
    
    API --> ConcertList
    API --> ConcertDetail
    API --> BookingList
    API --> BookingDetail
    API --> CreateBooking
    
    ConcertList --> Concert
    ConcertDetail --> Concert
    BookingList --> BookingModel
    BookingDetail --> BookingModel
    CreateBooking --> BookingModel
    CreateBooking --> Concert
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Vue as Vue.js Frontend
    participant API as Django REST API
    participant DB as SQLite Database

    Note over User, DB: Concert Browsing Flow
    User->>Vue: Visit Home Page
    Vue->>API: GET /api/concerts/
    API->>DB: SELECT * FROM concerts
    DB-->>API: Concert Data
    API-->>Vue: JSON Response
    Vue-->>User: Display Concert Grid

    Note over User, DB: Concert Booking Flow
    User->>Vue: Click "Book Now"
    Vue->>API: GET /api/concerts/{id}/
    API->>DB: SELECT concert details
    DB-->>API: Concert Data
    API-->>Vue: Concert Details
    Vue-->>User: Show Booking Form
    
    User->>Vue: Submit Booking Form
    Vue->>API: POST /api/bookings/
    API->>DB: INSERT booking record
    API->>DB: UPDATE concert tickets
    DB-->>API: Success
    API-->>Vue: Booking Confirmation
    Vue-->>User: Show Success Page
```

## Technology Stack Architecture

```mermaid
graph TB
    subgraph "Frontend Stack"
        Vue3[Vue.js 3]
        VueRouter[Vue Router 4]
        Axios[Axios HTTP Client]
        Bootstrap5[Bootstrap 5]
        FontAwesome6[Font Awesome 6]
    end

    subgraph "Backend Stack"
        Django4[Django 4.2]
        DRF[Django REST Framework]
        CORS[Django CORS Headers]
        SQLite3[SQLite 3]
    end

    subgraph "Development Tools"
        VueCLI[Vue CLI]
        DjangoAdmin[Django Admin]
        NPM[NPM Package Manager]
        PIP[PIP Package Manager]
    end

    subgraph "Deployment"
        DevServer[Development Servers]
        StaticFiles[Static File Serving]
        API_CORS[CORS Configuration]
    end

    Vue3 --> VueRouter
    Vue3 --> Axios
    Vue3 --> Bootstrap5
    Vue3 --> FontAwesome6
    
    Django4 --> DRF
    Django4 --> CORS
    Django4 --> SQLite3
    
    VueCLI --> Vue3
    DjangoAdmin --> Django4
    NPM --> VueCLI
    PIP --> Django4
    
    DevServer --> Vue3
    DevServer --> Django4
    StaticFiles --> Bootstrap5
    API_CORS --> CORS
```

## API Endpoint Architecture

```mermaid
graph LR
    subgraph "Concert Endpoints"
        GET_Concerts[GET /api/concerts/]
        GET_Concert[GET /api/concerts/{id}/]
        POST_Concert[POST /api/concerts/]
    end

    subgraph "Booking Endpoints"
        POST_Booking[POST /api/bookings/]
        GET_Bookings[GET /api/bookings/list/]
        GET_Booking[GET /api/bookings/{id}/]
    end

    subgraph "Admin Endpoints"
        Admin_Panel[/admin/]
        Admin_Concerts[/admin/concerts/concert/]
        Admin_Bookings[/admin/concerts/booking/]
    end

    GET_Concerts --> ConcertModel[(Concert Model)]
    GET_Concert --> ConcertModel
    POST_Concert --> ConcertModel
    
    POST_Booking --> BookingModel[(Booking Model)]
    GET_Bookings --> BookingModel
    GET_Booking --> BookingModel
    
    Admin_Panel --> Admin_Concerts
    Admin_Panel --> Admin_Bookings
    Admin_Concerts --> ConcertModel
    Admin_Bookings --> BookingModel
```

## Security & CORS Configuration

```mermaid
graph TB
    subgraph "Frontend (localhost:8080)"
        VueApp[Vue.js Application]
    end

    subgraph "Backend (localhost:8000)"
        DjangoAPI[Django REST API]
        CORS_Middleware[CORS Middleware]
    end

    subgraph "Security Features"
        CSRF[CSRF Protection]
        Validation[Input Validation]
        Sanitization[Data Sanitization]
    end

    VueApp -->|HTTP Requests| CORS_Middleware
    CORS_Middleware --> DjangoAPI
    DjangoAPI --> CSRF
    DjangoAPI --> Validation
    DjangoAPI --> Sanitization
    
    note1[CORS allows cross-origin requests from frontend to backend]
    note2[All user inputs are validated and sanitized]
    note3[CSRF protection enabled for admin interface]
```
