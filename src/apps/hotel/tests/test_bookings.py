import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.hotel.models import Room, Booking

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_room():
    return Room.objects.create(
        description="Тестовый улучшенный двуспальный номер",
        price_per_night="5000"
    )
@pytest.fixture
def sample_booking(sample_room):
    return Booking.objects.create(
        room=sample_room,
        start_date="2026-08-15",
        end_date="2026-08-20",
    )

def test_get_booking_list(api_client, sample_booking):
    url = reverse("booking-list-create")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["id"] == sample_booking.id

def test_create_booking_success(api_client, sample_room):
    url = reverse("booking-list-create")
    data = {
        "room": sample_room.id,
        "start_date": "2026-08-15",
        "end_date": "2026-08-20",
    }
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert Booking.objects.count() == 1

def test_get_booking_detail(api_client, sample_booking):
    url = reverse("booking-detail", kwargs={"booking_id": sample_booking.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

def test_delete_booking_success(api_client, sample_booking):
    url = reverse("booking-detail", kwargs={"booking_id": sample_booking.id})
    response = api_client.delete(url)

    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
    assert Booking.objects.count() == 0

def test_create_booking_overlapping_dates_fails(api_client, sample_booking):
    url = reverse("booking-list-create")
    data = {
        "room": sample_booking.room.id,
        "start_date": "2026-08-17",
        "end_date": "2026-08-22",
    }
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST