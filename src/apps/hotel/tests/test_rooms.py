import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.hotel.models import Room

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_room():
    return Room.objects.create(
        description="Тестовый уютный номер",
        price_per_night="3500.00"
    )

def test_get_room_list(api_client, sample_room):
    url = reverse("room-list-create")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["id"] == sample_room.id

def test_get_room_detail(api_client, sample_room):
    url = reverse("room-detail", kwargs={"room_id": sample_room.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == sample_room.id

def test_get_nonexistent_room(api_client, sample_room):
    url = reverse("room-detail", kwargs={"room_id": 999})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_room_success(api_client):
    url = reverse("room-list-create")
    initial_count = Room.objects.count()
    data = {
        "description": "Тестовый люкс номер",
        "price_per_night": "9000.50",
    }
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Room.objects.count() == 1
    assert Room.objects.get().description == data["description"]

    def test_create_room_invalid_data(api_client):
        url = reverse("room-list-create")
        data = {
            "description": "Номер с ошибкой",
            "price_per_night": "not_a_number",
        }
        response = api_client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "price_per_night" in response.data

    def test_get_room_detail_not_found(api_client):
        url = reverse("room-detail", kwargs={"room_id": 999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_delete_room_success(api_client, sample_room):
        url = reverse("room-detail", kwargs={"room_id": sample_room.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Room.objects.filter(id=sample_room.id).exists()
