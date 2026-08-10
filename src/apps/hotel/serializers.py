from rest_framework import serializers
from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price_per_night", "created_at"]

    def validate_price_per_night(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room", "start_date", "end_date"]

    def validate(self, attrs):
        room = attrs.get("room")
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if Booking.objects.filter(room=room, start_date__lt=end_date, end_date__gt=start_date).exists():
            raise serializers.ValidationError("Даты пересекаются.")

        return attrs