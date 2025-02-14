# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.timezone import now
import datetime


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('passenger', 'Passenger'),
        ('admin', 'Administrator'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='passenger')
    # Wallet system: users can add funds to this balance.
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username

class Bus(models.Model):
    bus_number = models.CharField(max_length=20)
    # In this phase, routes are fixed from Bus Stop A to Bus Stop B.
    route_from = models.CharField(max_length=50, default="Bus Stop A")
    route_to = models.CharField(max_length=50, default="Bus Stop B")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    seat_capacity = models.PositiveIntegerField()
    # We can use this field to track current available seats.
    available_seats = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2,default=100.00)

    def __str__(self):
        return f"{self.bus_number} ({self.route_from} -> {self.route_to})"

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Journey(models.Model):
    departure_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.departure_city} to {self.destination_city} on {self.departure_time}"
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    num_tickets = models.PositiveIntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user} for {self.journey}"
    
from django.conf import settings
class Passenger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

# Ticket Model - Passenger and Journey relationship
class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booked_on = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket {self.id} for {self.passenger.user.username}"

from datetime import timedelta
from django.utils import timezone

class Ticket(models.Model):
    # Other fields...

    def cancel(self):
        # Ensure the journey can only be canceled if it's at least 6 hours before departure
        if self.journey.departure_time - timezone.now() >= timedelta(hours=6):
            self.canceled = True
            self.save()
        else:
            raise ValueError("Cannot cancel the ticket less than 6 hours before departure")

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return now() < self.created_at + timedelta(minutes=10)  # OTP expires in 10 minutes

    def __str__(self):
        return f"{self.user.email} - {self.code}"

from django.conf import settings
from django.db import models
from django.utils.timezone import now
import datetime

def default_expiry():
    return now() + datetime.timedelta(minutes=5)

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def is_expired(self):
        return self.expires_at < now()

    def __str__(self):
        return f"{self.user.email} - {self.code}"


