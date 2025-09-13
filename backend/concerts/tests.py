import os
from django.test import TestCase, override_settings
from django.urls import reverse, NoReverseMatch
from django.conf import settings
from django.db import connections

def database_exists():
    """Check if the test database exists and is accessible."""
    try:
        connections['default'].ensure_connection()
        return True
    except Exception:
        return False

@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'test_db'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
)
class ConcertModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not database_exists():
            raise Exception("Database connection failed. Check your database settings.")

    def test_sample(self):
        """Test that 1 + 1 equals 2."""
        self.assertEqual(1 + 1, 2)

@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'test_db'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
)
class ConcertViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not database_exists():
            raise Exception("Database connection failed. Check your database settings.")
    
    def setUp(self):
        # Create a test static directory if it doesn't exist
        self.test_static_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
        os.makedirs(self.test_static_dir, exist_ok=True)
    
    def test_homepage_status_code(self):
        """Test that the homepage loads successfully."""
        urls_to_test = ['/']
        try:
            urls_to_test.append(reverse('home'))
        except NoReverseMatch:
            pass
        
        for url in urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn(
                    response.status_code, 
                    [200, 301, 302],  # 301 is for permanent redirects
                    f"Failed for URL: {url}. Status code: {response.status_code}"
                )

# Add a simple test function to verify the test discovery
def test_database_access():
    """Simple test to verify database access works."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        # Just verify we can query the database
        User.objects.count()
        assert True
    except Exception as e:
        assert False, f"Database access failed: {str(e)}"
