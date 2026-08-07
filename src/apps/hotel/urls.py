from django.urls import path

from apps.hotel.views import (
    RoomListCreateAPIView,
    RoomDetailAPIView,
    BookingListCreateAPIView,
    BookingDetailAPIView,
)


urlpatterns = [
    path("rooms/", RoomListCreateAPIView.as_view(), name="room-list-create"),
    path("rooms/<int:room_id>/", RoomDetailAPIView.as_view(), name="room-detail"),
    path("bookings/", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path("bookings/<int:booking_id>/", BookingDetailAPIView.as_view(), name="booking-detail"),
]