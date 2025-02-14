# core/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Journey  # Import the Journey model
from core.models import Journey

class PassengerLoginView(LoginView):
    template_name = 'core/passenger_login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if user.user_type != 'passenger':
            messages.error(self.request, "You are not authorized to log in as a passenger.")
            return self.form_invalid(form)
        return super().form_valid(form)

class AdminLoginView(LoginView):
    template_name = 'core/admin_login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if user.user_type != 'admin':
            messages.error(self.request, "You are not authorized to log in as an administrator.")
            return self.form_invalid(form)
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    next_page = '/'  # Redirect to home page after logout

def index(request):
     return render(request, 'index.html')

# core/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Bus, Booking

@staff_member_required  # Ensures only admin can access this view
def view_bookings(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    bookings = Booking.objects.filter(bus=bus)
    
    context = {
        'bus': bus,
        'bookings': bookings,
    }
    return render(request, 'core/view_bookings.html', context)

# core/views.py

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import BusForm

@staff_member_required
def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            bus = form.save(commit=False)
            bus.save()
            # Redirect to the bus list or another relevant page
            return redirect('bus_list')  # You can adjust this to any other view
    else:
        form = BusForm()

    context = {
        'form': form
    }
    return render(request, 'core/add_bus.html', context)

# core/views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Bus, Booking

@staff_member_required
def cancel_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)

    # Get all bookings related to the bus
    bookings = Booking.objects.filter(bus=bus)

    # Refund all the tickets for this bus
    for booking in bookings:
        # Add the refunded amount back to the user's wallet
        booking.user.wallet_balance += booking.total_amount
        booking.user.save()

        # You may choose to either delete the booking or mark it as canceled
        booking.delete()  # Deleting the booking record

    # Optionally, you can mark the bus as canceled instead of deleting it.
    bus.delete()  # If you want to remove the bus entirely

    messages.success(request, f"Bus {bus.bus_number} has been canceled, and refunds have been issued.")
    return redirect('bus_list')  # Redirect to the list of buses or another page

# core/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Bus
from .forms import BusUpdateForm

@staff_member_required
def update_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == 'POST':
        form = BusUpdateForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, f"Bus {bus.bus_number} has been updated successfully.")
            return redirect('bus_list')  # Redirect to a list of buses
    else:
        form = BusUpdateForm(instance=bus)

    context = {
        'form': form,
        'bus': bus
    }
    return render(request, 'core/update_bus.html', context)

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Or a simple response for testing


from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Bus Booking System!")

from django.shortcuts import render
from .models import Ticket

def view_journeys(request):
    # Get the logged-in passenger
    passenger = request.user.passenger
    # Get upcoming and past journeys
    upcoming_journeys = Ticket.objects.filter(passenger=passenger, canceled=False, journey__departure_time__gte=datetime.now())
    past_journeys = Ticket.objects.filter(passenger=passenger, canceled=False, journey__departure_time__lt=datetime.now())

    return render(request, 'core/journeys.html', {
        'upcoming_journeys': upcoming_journeys,
        'past_journeys': past_journeys,
    })

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Ticket

def cancel_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, passenger=request.user.passenger)

    try:
        ticket.cancel()
        return HttpResponse("Ticket canceled successfully")
    except ValueError as e:
        return HttpResponse(str(e), status=400)

from .forms import BusSearchForm
from .models import Journey

def search_buses(request):
    if request.method == 'GET':
        form = BusSearchForm(request.GET)
        if form.is_valid():
            departure_city = form.cleaned_data['departure_city']
            destination_city = form.cleaned_data['destination_city']
            buses = Journey.objects.filter(departure_city=departure_city, destination_city=destination_city).order_by('departure_time')
        else:
            buses = []

    return render(request, 'core/search_buses.html', {'form': form, 'buses': buses})

def book_ticket(request, journey_id):
    journey = get_object_or_404(Journey, id=journey_id)
    passenger = request.user.passenger

    if passenger.wallet_balance >= 100:  # Assuming 100 is the ticket price
        # Proceed to book the ticket
        ticket = Ticket.objects.create(passenger=passenger, journey=journey, seat_number=1)
        passenger.wallet_balance -= 100  # Deduct the ticket price
        passenger.save()
        return HttpResponse(f"Ticket booked for {journey.departure_city} to {journey.destination_city}")
    else:
        return HttpResponse("Insufficient balance", status=400)

from django.shortcuts import render
from .models import Journey  # Import your Journey model

def view_journeys(request):
    # Assuming you have a Journey model related to users
    journeys = Journey.objects.filter(user=request.user)  # Get journeys of the logged-in user
    return render(request, 'journeys/view_journeys.html', {'journeys': journeys})

# core/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')  # Ensure this template exists


from django.shortcuts import render, get_object_or_404
from .models import Journey  # Make sure this import is present

def view_journeys(request):
    journeys = Journey.objects.all()
    return render(request, 'core/journeys.html', {'journeys': journeys})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import OTP
from django.utils.timezone import now

@login_required
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        otp_instance = OTP.objects.filter(user=request.user, code=entered_otp).first()

        if otp_instance and otp_instance.is_valid():
            otp_instance.delete()  # OTP is valid, remove it
            return redirect("home")
        else:
            return render(request, "core/verify_otp.html", {"error": "Invalid or expired OTP."})

    return render(request, "core/verify_otp.html")

from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return render(request, "core/verification_failed.html")

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from core.utils import send_otp_email

User = get_user_model()

def register_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(email=email, password=password, is_active=False)  # Inactive until OTP is verified
        send_otp_email(user)
        messages.success(request, "An OTP has been sent to your email. Please verify your account.")
        return redirect("verify_otp")

    return render(request, "register.html")

from django.utils.timezone import now
from django.contrib.auth import login
from core.models import OTP

def verify_otp(request):
    if request.method == "POST":
        email = request.POST["email"]
        otp_code = request.POST["otp_code"]

        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user).latest("created_at")  # Get the latest OTP

            if otp.is_valid() and otp.code == otp_code:
                user.is_active = True
                user.save()
                login(request, user)
                messages.success(request, "OTP verified successfully! You are now logged in.")
                return redirect("home")

            else:
                messages.error(request, "Invalid or expired OTP. Please try again.")
        
        except (User.DoesNotExist, OTP.DoesNotExist):
            messages.error(request, "Invalid credentials.")

    return render(request, "verify_otp.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OTP
from .forms import OTPForm

def verify_otp(request):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data["otp"]
            otp = OTP.objects.filter(code=otp_code, user=request.user).first()
            
            if otp and not otp.is_expired():
                otp.delete()  # OTP is valid, delete it after use
                messages.success(request, "OTP verified successfully!")
                return redirect("home")  # Redirect to homepage or dashboard
            else:
                messages.error(request, "Invalid or expired OTP.")

    else:
        form = OTPForm()

    return render(request, "core/verify_otp.html", {"form": form})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.forms import BookingForm
from core.utils import send_email_notification

@login_required
def book_ticket(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            
            # Send email notification
            subject = "Booking Confirmation"
            message = f"Dear {request.user.username},\n\nYour booking for journey {booking.journey} is confirmed.\n\nThank you!"
            recipient_list = [request.user.email]
            send_email_notification(subject, message, recipient_list)

            return redirect("booking_success")  # Redirect to success page

    else:
        form = BookingForm()

    return render(request, "core/book_ticket.html", {"form": form})

