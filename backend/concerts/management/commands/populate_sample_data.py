from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from concerts.models import Concert

class Command(BaseCommand):
    help = 'Populate the database with sample concert data'

    def handle(self, *args, **options):
        # Clear existing concerts
        Concert.objects.all().delete()
        
        # Sample concert data
        sample_concerts = [
            {
                'title': 'Rock Night Live',
                'artist': 'The Electric Guitars',
                'venue': 'Madison Square Garden',
                'date': timezone.now() + timedelta(days=20),
                'price': 75.00,
                'available_tickets': 500,
                'description': 'An electrifying rock concert featuring the best hits from The Electric Guitars.',
                'image_url': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400'
            },
            {
                'title': 'Jazz Under the Stars',
                'artist': 'Smooth Jazz Ensemble',
                'venue': 'Blue Note',
                'date': timezone.now() + timedelta(days=27),
                'price': 45.00,
                'available_tickets': 200,
                'description': 'A smooth jazz evening under the open sky with talented musicians.',
                'image_url': 'https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=400'
            },
            {
                'title': 'Pop Sensation Tour',
                'artist': 'Luna Star',
                'venue': 'Arena Stadium',
                'date': timezone.now() + timedelta(days=40),
                'price': 120.00,
                'available_tickets': 1000,
                'description': 'The biggest pop sensation of the year brings her world tour to your city.',
                'image_url': 'https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=400'
            },
            {
                'title': 'Classical Symphony Night',
                'artist': 'City Orchestra',
                'venue': 'Concert Hall',
                'date': timezone.now() + timedelta(days=47),
                'price': 60.00,
                'available_tickets': 300,
                'description': 'Experience the beauty of classical music with our renowned city orchestra.',
                'image_url': 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=400'
            }
        ]
        
        for concert_data in sample_concerts:
            concert = Concert.objects.create(**concert_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created concert: {concert.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {len(sample_concerts)} concerts')
        )
