from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeOperators
from django.db.models import Func
from django.db import models


class Room(models.Model):
    description = models.TextField(default="")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комната {self.id}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=["room", "start_date"], name="booking_index"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=models.F('start_date')),
                name="booking_end_date_after_start_date",
            ),
            ExclusionConstraint(
                name="prevent_booking_overlaps",
                expressions=[
                    ("room", "="),
                    (Func("start_date", "end_date", function="daterange"), RangeOperators.OVERLAPS),
                ],
            ),
        ]