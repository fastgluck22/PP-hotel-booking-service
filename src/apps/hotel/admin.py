from django.contrib import admin
from apps.hotel.models import Room, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "price_per_night")
    list_display_links = ("id", "description")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "start_date", "end_date")
    list_display_links = ("id", "room")
