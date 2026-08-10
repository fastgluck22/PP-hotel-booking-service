from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer

class RoomListCreateAPIView(APIView):
    def get(self, request):
        sort_mapping = {"id": "id",
                        "-id": "-id",
                        "price": "price_per_night",
                        "-price": "-price_per_night",
                        "created_at": "created_at",
                        "-created_at": "-created_at",
        }

        sort_by = request.query_params.get("sort")
        order_field = sort_mapping.get(sort_by, "id")
        rooms = Room.objects.all().order_by(order_field)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_rooms = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(paginated_rooms, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailAPIView(APIView):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingListCreateAPIView(APIView):
    def get(self, request):
        bookings = Booking.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 15
        paginated_bookings = paginator.paginate_queryset(bookings, request)
        serializer = BookingSerializer(paginated_bookings, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailAPIView(APIView):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)