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
        fields = ["room", "start_date", "end_date"]

    def validate_date(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if end_date <= start_date:
            raise serializers.ValidationError({"end_date":"Дата окончания бронирования должна быть позже даты начала"})
        return end_date