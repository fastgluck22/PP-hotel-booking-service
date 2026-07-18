from django.urls import path
from apps.hotel.views import (
    create_room,
    get_rooms,
    delete_rooms,
    create_booking,
    delete_booking,
    get_booking,
)
from apps.hotel.admin import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/create", create_room),
    path("rooms/list", get_rooms),
    path("rooms/delete/<int:room_id>", delete_rooms),
    path("bookings/create", create_booking),
    path("bookings/delete/<int:booking_id>", delete_booking),
    path("bookings/list", get_booking),
]
