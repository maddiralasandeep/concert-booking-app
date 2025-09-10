from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
import os

# Add this decorator to avoid collecting static files during tests
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ConcertModelTest(TestCase):
    def test_sample(self):
        """Test that 1 + 1 equals 2."""
        self.assertEqual(1 + 1, 2)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ConcertViewTest(TestCase):
    def setUp(self):
        # Create a test static directory if it doesn't exist
        self.test_static_dir = os.path.join(settings.BASE_DIR, 'staticfiles')
        os.makedirs(self.test_static_dir, exist_ok=True)
    
    def test_homepage_status_code(self):
        """Test that the homepage loads successfully."""
        # Test both root URL and named URL pattern if it exists
        urls_to_test = ['/', reverse('home')] if 'home' in [url.name for url in __import__('django.urls').urls.urlpatterns if hasattr(url, 'name')] else ['/']
        
        for url in urls_to_test:
            with self.subTest(url=url):
                response = self.client.get(url)
                # Accept both 200 (success) and 302 (redirect) as valid responses
                self.assertIn(response.status_code, [200, 302], f"Failed for URL: {url}")
