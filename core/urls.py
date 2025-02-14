# core/urls.py
from django.urls import path, include
from django.contrib import admin
from .import views
from .views import PassengerLoginView, AdminLoginView, UserLogoutView, index
from core.models import Journey
urlpatterns = [
    path('', views.home, name='home'),
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('journeys/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('admin/update-bus/<int:bus_id>/', views.update_bus, name='update_bus'), 
    path('passenger/login/', PassengerLoginView.as_view(), name='passenger_login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('cancel-ticket/<int:ticket_id>/', views.cancel_ticket, name='cancel_ticket'),
    path('search/', views.search_buses, name='search_buses'),
    path('book-ticket/<int:journey_id>/', views.book_ticket, name='book_ticket'),
]

# core/urls.py
from .views import view_bookings

urlpatterns = [
    # Other URL patterns
    path('admin/view-bookings/<int:bus_id>/', view_bookings, name='view_bookings'),
]

# core/urls.py
from .views import add_bus

urlpatterns = [
    # Other URL patterns
    path('admin/add-bus/', add_bus, name='add_bus'),
]

# core/urls.py
from .views import cancel_bus

urlpatterns = [
    # Other URL patterns
    path('admin/cancel-bus/<int:bus_id>/', cancel_bus, name='cancel_bus'),
]

# core/urls.py
from .views import update_bus

urlpatterns = [
    # Other URL patterns
    path('admin/update-bus/<int:bus_id>/', update_bus, name='update_bus'),
]

from django.shortcuts import render, get_object_or_404
from .models import Bus

def update_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == "POST":
        # Process form data to update bus
        pass
    return render(request, 'update_bus.html', {'bus': bus})

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('journeys/', views.view_journeys, name='view_journeys'),
]

from django.urls import path
from core.views import register_user, verify_otp

urlpatterns = [
    path("register/", register_user, name="register"),
    path("verify-otp/", verify_otp, name="verify_otp"),
]

from django.urls import path
from .views import verify_otp

urlpatterns = [
    path("verify-otp/", verify_otp, name="verify_otp"),
]

from django.urls import path
from core.views import book_ticket

urlpatterns = [
    path("book/", book_ticket, name="book_ticket"),
]
