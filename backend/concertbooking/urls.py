from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home_view(request):
    """Default home view that returns a simple JSON response."""
    return JsonResponse({
        'status': 'success',
        'message': 'Welcome to Concert Booking API',
        'endpoints': {
            'api': '/api/',
            'admin': '/admin/'
        }
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('concerts.urls')),
]
