import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from apps.hotel.models import Room, Booking


@csrf_exempt
def create_room(request):
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                data = request.POST

            description = data.get("description")
            price_per_night = data.get("price_per_night")

            if not description or not price_per_night:
                return JsonResponse(
                    {"ошибка": "Укажите описание и цену за ночь"},
                    status=400,
                    json_dumps_params={"ensure_ascii": False},
                )
            try:
                price_per_night = float(price_per_night)
            except ValueError:
                return JsonResponse(
                    {"ошибка": "Цена должна быть числом"},
                    status=400,
                    json_dumps_params={"ensure_ascii": False},
                )

            room = Room.objects.create(
                description=description, price_per_night=float(price_per_night)
            )
            return JsonResponse(
                {"room_id": room.id},
                status=201,
                json_dumps_params={"ensure_ascii": False},
            )

        except Exception as e:
            return JsonResponse(
                {"ошибка": str(e)},
                status=500,
                json_dumps_params={"ensure_ascii": False},
            )

    return JsonResponse(
        {"ошибка": "Разрешен только POST-метод"},
        status=405,
        json_dumps_params={"ensure_ascii": False},
    )


@csrf_exempt
def get_rooms(request):
    if request.method == "GET":
        try:
            sort_by = request.GET.get("sort")
            if sort_by in ["price", "-price", "id", "-id"]:
                if sort_by == "price":
                    rooms = Room.objects.all().order_by("price_per_night")
                elif sort_by == "-price":
                    rooms = Room.objects.all().order_by("-price_per_night")
                elif sort_by == "id":
                    rooms = Room.objects.all().order_by("id")
                elif sort_by == "-id":
                    rooms = Room.objects.all().order_by("-id")

            else:
                rooms = Room.objects.all().order_by("id")

            rooms_list = []
            for room in rooms:
                rooms_list.append(
                    {
                        "id": room.id,
                        "description": room.description,
                        "price_per_night": float(room.price_per_night),
                    }
                )
            return JsonResponse(
                {"rooms": rooms_list},
                status=200,
                json_dumps_params={"ensure_ascii": False},
            )
        except Exception as e:
            return JsonResponse(
                {"ошибка": str(e)},
                status=500,
                json_dumps_params={"ensure_ascii": False},
            )
    return JsonResponse(
        {
            "ошибка": "Разрешен только GET-метод",
        },
        status=405,
        json_dumps_params={"ensure_ascii": False},
    )


@csrf_exempt
def delete_rooms(request, room_id):
    if request.method == "DELETE":
        try:
            room = get_object_or_404(Room, id=room_id)
            room.delete()
            return JsonResponse(
                {"сообщение": f"Комната {room_id} и все брони успешно удалены"},
                status=200,
                json_dumps_params={"ensure_ascii": False},
            )

        except Exception as e:
            return JsonResponse(
                {"ошибка": str(e)},
                status=500,
                json_dumps_params={"ensure_ascii": False},
            )

    return JsonResponse(
        {
            "ошибка": "Разрешен только DELETE-метод",
        },
        status=405,
        json_dumps_params={"ensure_ascii": False},
    )


@csrf_exempt
def create_booking(request):
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                data = request.POST

            room_id = data.get("room_id")
            start_date = data.get("start_date")
            end_date = data.get("end_date")

            if not all([room_id, start_date, end_date]):
                return JsonResponse(
                    {"ошибка": "Введите номер комнаты, дату заезда и выезда"},
                    status=400,
                    json_dumps_params={"ensure_ascii": False},
                )

            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse(
                    {"ошибка": "Неверный формат даты. Ожидается ГГГГ-ММ-ДД"},
                    status=400,
                    json_dumps_params={"ensure_ascii": False},
                )

            if end_date <= start_date:
                return JsonResponse(
                    {"ошибка": "Дата выезда должна быть позже даты заезда"},
                    status=400,
                    json_dumps_params={"ensure_ascii": False},
                )

            room = get_object_or_404(Room, id=room_id)
            new_booking = Booking.objects.create(
                room=room, start_date=start_date, end_date=end_date
            )
            return JsonResponse(
                {
                    "сообщение": "Комната забронирована.",
                    "new_booking": {
                        "id": new_booking.id,
                        "room_id": room.id,
                        "start_date": str(new_booking.start_date),
                        "end_date": str(new_booking.end_date),
                    },
                },
                status=201,
                json_dumps_params={"ensure_ascii": False},
            )

        except json.decoder.JSONDecodeError:
            return JsonResponse(
                {"ошибка": "Некорректный JSON."},
                status=400,
                json_dumps_params={"ensure_ascii": False},
            )
        except Exception as e:
            return JsonResponse(
                {"ошибка": str(e)},
                status=500,
                json_dumps_params={"ensure_ascii": False},
            )

    return JsonResponse(
        {"ошибка": "Разрешен только POST-метод"},
        status=405,
        json_dumps_params={"ensure_ascii": False},
    )


@csrf_exempt
def delete_booking(request, booking_id):
    if request.method == "DELETE":
        try:
            booking = get_object_or_404(Booking, id=booking_id)
            booking.delete()
            return JsonResponse(
                {"сообщение": f"Бронирование {booking_id} успешно удалено."},
                status=200,
                json_dumps_params={"ensure_ascii": False},
            )
        except Exception as e:
            return JsonResponse(
                {"ошибка": str(e)},
                status=500,
                json_dumps_params={"ensure_ascii": False},
            )

    return JsonResponse(
        {
            "ошибка": "Разрешен только DELETE-метод",
        },
        status=405,
        json_dumps_params={"ensure_ascii": False},
    )


@csrf_exempt
def get_booking(request):
    if request.method == "GET":
        try:
            room_id = request.GET.get("room_id")
            if not room_id:
                return JsonResponse(
                    {"ошибка": "Укажите ID комнаты"},
                    status=400,
                    json_dumps_params={"ensure_ascii": False},
                )

            bookings = Booking.objects.filter(room_id=room_id).order_by("start_date")
            booking_list = []

            for b in bookings:
                booking_list.append(
                    {
                        "id": b.id,
                        "room_id": b.room.id,
                        "start_date": str(b.start_date),
                        "end_date": str(b.end_date),
                    }
                )

            return JsonResponse(
                {"bookings": booking_list},
                status=200,
                json_dumps_params={"ensure_ascii": False},
            )
        except Exception as e:
            return JsonResponse(
                {"ошибка": str(e)},
                status=500,
                json_dumps_params={"ensure_ascii": False},
            )

    return JsonResponse(
        {
            "ошибка": "Разрешен только GET-метод",
        },
        status=405,
        json_dumps_params={"ensure_ascii": False},
    )
