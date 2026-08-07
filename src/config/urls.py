from django.contrib import admin
from django.urls import include, path

from apps.hotel.views import (
    RoomListCreateAPIView,
    RoomDetailAPIView,
    BookingListCreateAPIView,
    BookingDetailAPIView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.hotel.urls")),
]
