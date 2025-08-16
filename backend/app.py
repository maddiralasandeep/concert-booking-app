from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///concerts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Concert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'venue': self.venue,
            'date': self.date.isoformat(),
            'price': self.price,
            'available_tickets': self.available_tickets,
            'description': self.description,
            'image_url': self.image_url
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    tickets_booked = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    
    concert = db.relationship('Concert', backref=db.backref('bookings', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'concert_id': self.concert_id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'tickets_booked': self.tickets_booked,
            'booking_date': self.booking_date.isoformat(),
            'total_amount': self.total_amount,
            'concert': self.concert.to_dict() if self.concert else None
        }

# Routes
@app.route('/api/concerts', methods=['GET'])
def get_concerts():
    concerts = Concert.query.all()
    return jsonify([concert.to_dict() for concert in concerts])

@app.route('/api/concerts/<int:concert_id>', methods=['GET'])
def get_concert(concert_id):
    concert = Concert.query.get_or_404(concert_id)
    return jsonify(concert.to_dict())

@app.route('/api/concerts', methods=['POST'])
def create_concert():
    data = request.get_json()
    
    concert = Concert(
        title=data['title'],
        artist=data['artist'],
        venue=data['venue'],
        date=datetime.fromisoformat(data['date']),
        price=data['price'],
        available_tickets=data['available_tickets'],
        description=data.get('description', ''),
        image_url=data.get('image_url', '')
    )
    
    db.session.add(concert)
    db.session.commit()
    
    return jsonify(concert.to_dict()), 201

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    concert = Concert.query.get_or_404(data['concert_id'])
    
    if concert.available_tickets < data['tickets_booked']:
        return jsonify({'error': 'Not enough tickets available'}), 400
    
    total_amount = concert.price * data['tickets_booked']
    
    booking = Booking(
        concert_id=data['concert_id'],
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        tickets_booked=data['tickets_booked'],
        total_amount=total_amount
    )
    
    # Update available tickets
    concert.available_tickets -= data['tickets_booked']
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify(booking.to_dict()), 201

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings])

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict())

def init_sample_data():
    """Initialize the database with sample concert data"""
    if Concert.query.count() == 0:
        sample_concerts = [
            {
                'title': 'Rock Night Live',
                'artist': 'The Electric Guitars',
                'venue': 'Madison Square Garden',
                'date': datetime(2024, 8, 15, 20, 0),
                'price': 75.00,
                'available_tickets': 500,
                'description': 'An electrifying rock concert featuring the best hits from The Electric Guitars.',
                'image_url': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400'
            },
            {
                'title': 'Jazz Under the Stars',
                'artist': 'Smooth Jazz Ensemble',
                'venue': 'Blue Note',
                'date': datetime(2025, 8, 22, 19, 30),
                'price': 45.00,
                'available_tickets': 200,
                'description': 'A smooth jazz evening under the open sky with talented musicians.',
                'image_url': 'https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=400'
            },
            {
                'title': 'Pop Sensation Tour',
                'artist': 'Luna Star',
                'venue': 'Arena Stadium',
                'date': datetime(2024, 9, 5, 21, 0),
                'price': 120.00,
                'available_tickets': 1000,
                'description': 'The biggest pop sensation of the year brings her world tour to your city.',
                'image_url': 'https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=400'
            },
            {
                'title': 'Classical Symphony Night',
                'artist': 'City Orchestra',
                'venue': 'Concert Hall',
                'date': datetime(2024, 9, 12, 18, 0),
                'price': 60.00,
                'available_tickets': 300,
                'description': 'Experience the beauty of classical music with our renowned city orchestra.',
                'image_url': 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=400'
            }
        ]
        
        for concert_data in sample_concerts:
            concert = Concert(**concert_data)
            db.session.add(concert)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
    app.run(debug=True, port=5000)
