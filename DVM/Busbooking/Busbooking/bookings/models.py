from django.db import models
from django.contrib.auth.models import user
from django.db import models

class Wallet(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

class Bus(models.Model):
    bus_number=models.CharField(max_length=10)
    source=models.CharField(max_lenth=100)
    destination=models.Charfield(max_length=100)
    departure_time=models.DateTimeField()
    arrival_time=models.DateTimeField()
    seats_available=models.IntegerField()
    fare=models.DecimalField(max_digits=10,decimal_places=2)

class Booking(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    passenger=models.ForeignKey(User,on_delete=models.CASCADE)
    seats_booked=models.IntegerField()
    booking_time=models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        if self.seats_booked>self.bus.seats_available:
            raise ValueError("Not enough seats available")
        self.bus.seats_available-=self.seats_booked
        self.bus.save()
        super().save(*args,**kwargs)
        