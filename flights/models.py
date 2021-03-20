"""This script creates models to be used in the application."""
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Flight(models.Model):
    """class object to provode flight details."""
    flight_no = models.IntegerField(primary_key=True, default=1007)
    airline_name = models.CharField(max_length=50)
    no_of_seats = models.IntegerField(default=0)
    source = models.CharField(max_length=50)
    source_code = models.CharField(max_length=3)
    destination = models.CharField(max_length=50)
    destination_code = models.CharField(max_length=3)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    cost = models.IntegerField(default=500)

    def __str__(self):
        return f"Flight: {self.flight_no} from {self.source} to {self.destination}"


class User(AbstractUser):
    """class for creating users and roles."""
    USER_TYPE_CHOICES = (
      (1, 'flightstaff'),
      (2, 'admin')
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=1
    )


class Staff(models.Model):
    """class to create staff users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    id = models.IntegerField(primary_key=True)
    flight_no = models.ManyToManyField(
        Flight, blank=True, related_name='staffs'
    )

    def __str__(self):
        return f"{self.user}"


class Passenger(models.Model):
    """Class to define passenger details."""
    pnr = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    ppno = models.CharField(max_length=50)
    dob = models.DateField(default=1/1/1990)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    flight_no = models.ForeignKey(
        Flight, on_delete=models.CASCADE, default=1007,
        related_name='passengers'
    )
    checked_in_status = models.BooleanField(default=0)
    booked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default='moha'
    )

    def __str__(self):
        return f"{self.pnr} - {self.first_name} {self.last_name}"
