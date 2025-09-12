import os
import sys
import pytest
from pathlib import Path

import django
from django.conf import settings

def pytest_configure():
    """Configure pytest for Django tests."""
    # Add the project to the Python path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR))
    
    # Configure Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concertbooking.settings')
    
    # Initialize Django
    django.setup()

@pytest.fixture(scope='session')
def django_db_setup():
    """Set up the test database."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
    # Run migrations
    from django.core.management import call_command
    call_command('migrate', '--noinput')

@pytest.fixture
def client():
    """A Django test client instance."""
    from django.test import Client
    return Client()
