from django.test import TestCase
from django.urls import reverse

class ConcertModelTest(TestCase):
    def test_sample(self):
        """Test that 1 + 1 equals 2."""
        self.assertEqual(1 + 1, 2)

class ConcertViewTest(TestCase):
    def test_homepage_status_code(self):
        """Test that the homepage loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
