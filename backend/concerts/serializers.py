from rest_framework import serializers
from .models import Concert, Booking

class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['id', 'title', 'artist', 'venue', 'date', 'price', 
                 'available_tickets', 'description', 'image_url', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    concert = ConcertSerializer(read_only=True)
    concert_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'concert', 'concert_id', 'customer_name', 
                 'customer_email', 'tickets_booked', 'booking_date', 
                 'total_amount']
        read_only_fields = ['id', 'booking_date', 'total_amount']
    
    def validate(self, data):
        concert_id = data.get('concert_id')
        tickets_booked = data.get('tickets_booked')
        
        try:
            concert = Concert.objects.get(id=concert_id)
        except Concert.DoesNotExist:
            raise serializers.ValidationError("Concert does not exist.")
        
        if concert.available_tickets < tickets_booked:
            raise serializers.ValidationError(
                f"Only {concert.available_tickets} tickets available."
            )
        
        return data
    
    def create(self, validated_data):
        concert_id = validated_data.pop('concert_id')
        concert = Concert.objects.get(id=concert_id)
        
        # Calculate total amount
        validated_data['total_amount'] = concert.price * validated_data['tickets_booked']
        validated_data['concert'] = concert
        
        # Create booking
        booking = Booking.objects.create(**validated_data)
        
        # Update available tickets
        concert.available_tickets -= validated_data['tickets_booked']
        concert.save()
        
        return booking

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['concert_id', 'customer_name', 'customer_email', 'tickets_booked']
