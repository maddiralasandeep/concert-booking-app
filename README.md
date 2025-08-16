# ConcertBook - Concert Booking SPA

A modern single-page application for booking concert tickets, built with Vue.js frontend and Django backend.

## Features

- 🎵 Browse upcoming concerts
- 🔍 Search concerts by title, artist, or venue
- 🎫 Book tickets with real-time availability
- 📱 Responsive design for all devices
- 💳 Booking management and confirmation
- 📊 Admin panel for concert management

## Tech Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Bootstrap 5** - CSS framework for responsive design
- **Font Awesome** - Icons

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - API development
- **SQLite** - Database (easily switchable to PostgreSQL/MySQL)
- **Django CORS Headers** - Cross-origin resource sharing

## Project Structure

```
windsurf-project/
├── backend/                    # Django backend
│   ├── concertbooking/        # Django project settings
│   ├── concerts/              # Concerts app
│   │   ├── models.py          # Concert and Booking models
│   │   ├── serializers.py     # API serializers
│   │   ├── views.py           # API views
│   │   └── urls.py            # API endpoints
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Vue.js frontend
│   ├── src/
│   │   ├── views/             # Vue components/pages
│   │   ├── router/            # Vue Router configuration
│   │   ├── services/          # API service layer
│   │   ├── App.vue            # Main app component
│   │   └── main.js            # App entry point
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   └── vue.config.js          # Vue CLI configuration
└── README.md                  # Project documentation
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create sample data:
```bash
python manage.py populate_sample_data
```

7. (Optional) Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

8. Start the Django development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000/`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the Vue.js development server:
```bash
npm run serve
```

The frontend application will be available at `http://localhost:8080/`

## API Endpoints

### Concerts
- `GET /api/concerts/` - List all concerts
- `GET /api/concerts/{id}/` - Get concert details
- `POST /api/concerts/` - Create new concert (admin)

### Bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/list/` - List all bookings
- `GET /api/bookings/{id}/` - Get booking details

## Usage

1. **Browse Concerts**: Visit the home page to see all upcoming concerts
2. **Search**: Use the search bar to find specific concerts
3. **View Details**: Click on any concert to see detailed information
4. **Book Tickets**: Fill out the booking form with your details
5. **Confirmation**: Receive booking confirmation with all details
6. **Manage Bookings**: View all your bookings in the "My Bookings" section

## Development

### Adding New Concerts
You can add new concerts through:
1. Django Admin Panel: `http://localhost:8000/admin/`
2. API endpoint: `POST /api/concerts/`
3. Management command: Modify `populate_sample_data.py`

### Customization
- **Styling**: Modify Bootstrap classes in Vue components
- **API**: Extend Django models and serializers
- **Features**: Add new Vue components and routes

## Deployment

### Backend (Django)
- Configure production database (PostgreSQL recommended)
- Set `DEBUG = False` in settings
- Configure static files serving
- Use WSGI server like Gunicorn

### Frontend (Vue.js)
- Build for production: `npm run build`
- Serve static files with nginx or similar
- Update API base URL for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please create an issue in the repository or contact the development team.
