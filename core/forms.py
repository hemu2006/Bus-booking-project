# core/forms.py
from django import forms
from .models import Bus
from core.models import Journey


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_number', 'route_from', 'route_to', 'departure_time', 'arrival_time', 'seat_capacity', 'available_seats']

    operating_days = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ],
        label="Days of the Week the Bus Operates"
    )

# core/forms.py
from django import forms
from .models import Bus

class BusUpdateForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_number', 'route_from', 'route_to', 'departure_time', 'arrival_time', 'seat_capacity', 'available_seats', 'fare']

from django import forms

class BusSearchForm(forms.Form):
    departure_city = forms.CharField(max_length=100)
    destination_city = forms.CharField(max_length=100)

from django import forms

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))

from django import forms
from core.models import Booking, Journey

class BookingForm(forms.ModelForm):
    journey = forms.ModelChoiceField(queryset=Journey.objects.all(), empty_label="Select a Journey")
    num_tickets = forms.IntegerField(min_value=1, max_value=10, label="Number of Tickets")

    class Meta:
        model = Booking
        fields = ['journey', 'num_tickets']
