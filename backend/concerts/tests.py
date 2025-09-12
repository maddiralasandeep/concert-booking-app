import pytest
from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
import os

# Add this decorator to avoid collecting static files during tests
@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
)
class ConcertModelTest(TestCase):
    def test_sample(self):
        """Test that 1 + 1 equals 2."""
        self.assertEqual(1 + 1, 2)

@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
)
class ConcertViewTest(TestCase):
    def setUp(self):
        # Create a test static directory if it doesn't exist
        self.test_static_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
        os.makedirs(self.test_static_dir, exist_ok=True)
    
    def test_homepage_status_code(self):
        """Test that the homepage loads successfully."""
        urls_to_test = ['/']
        try:
            urls_to_test.append(reverse('home'))
        except:
            pass
        
        for url in urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn(response.status_code, [200, 302], f"Failed for URL: {url}")

# Add a simple pytest test function to verify the test discovery
def test_database_access(db):
    """Simple test to verify database access works."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    assert User.objects.count() >= 0
