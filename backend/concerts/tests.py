import pytest
from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
import os

# Add this decorator to avoid collecting static files during tests
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ConcertModelTest(TestCase):
    @pytest.mark.django_db
    def test_sample(self):
        """Test that 1 + 1 equals 2."""
        self.assertEqual(1 + 1, 2)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ConcertViewTest(TestCase):
    @pytest.mark.django_db
    def setUp(self):
        # Create a test static directory if it doesn't exist
        self.test_static_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
        os.makedirs(self.test_static_dir, exist_ok=True)
    
    @pytest.mark.django_db
    def test_homepage_status_code(self):
        """Test that the homepage loads successfully."""
        # Test both root URL and named URL pattern if it exists
        urls_to_test = ['/']
        try:
            urls_to_test.append(reverse('home'))
        except:
            pass
        
        for url in urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                # Accept both 200 (success) and 302 (redirect) as valid responses
                self.assertIn(response.status_code, [200, 302], f"Failed for URL: {url}")

# Add a simple pytest test function to verify the test discovery
@pytest.mark.django_db
def test_database_access():
    """Simple test to verify database access works."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    assert User.objects.count() >= 0
