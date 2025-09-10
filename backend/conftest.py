import os
import sys
from pathlib import Path

import django
from django.conf import settings

@pytest.mark.django_db
def pytest_configure():
    """Configure pytest for Django tests."""
    # Add the project to the Python path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR))
    
    # Configure Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'concertbooking.settings'
    os.environ['DJANGO_CONFIGURATION'] = 'Settings'
    
    # Initialize Django
    django.setup()
    
    # Ensure test database is ready
    from django.core.management import call_command
    call_command('migrate', '--noinput')
