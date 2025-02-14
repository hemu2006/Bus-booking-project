from django.core.mail import send_mail
from .models import OTP
import random
from django.conf import settings


def generate_otp(user):
    otp_code = str(random.randint(100000, 999999))
    OTP.objects.create(user=user, code=otp_code)

    send_mail(
        "Your OTP Code",
        f"Your OTP is {otp_code}. It will expire in 10 minutes.",
        "hemavardhan.juvvi@gmail.com",
        [user.email],
        fail_silently=False,
    )

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)

    verification_link = f"http://{current_site.domain}/verify-email/{uid}/{token}/"

    message = render_to_string("core/email_verification.html", {"link": verification_link})

    send_mail(
        "Verify Your Email",
        message,
        "hemavardhan.juvvi@gmail.com",
        [user.email],
        fail_silently=False,
    )

import random
from django.core.mail import send_mail
from django.utils.timezone import now
from core.models import OTP

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def send_otp_email(user):
    otp_code = generate_otp()
    OTP.objects.create(user=user, code=otp_code)

    subject = "Your OTP Code for Bus Booking System"
    message = f"Hello {user.email},\n\nYour OTP code is: {otp_code}.\n\nThis code is valid for 10 minutes."
    
    send_mail(subject, message, "hemavardhan.juvvi@gmail.com", [user.email])

from django.core.mail import send_mail
from django.utils.timezone import now
import random
from .models import OTP

def generate_otp(user):
    """Generates a 6-digit OTP and saves it to the database."""
    otp_code = str(random.randint(100000, 999999))
    otp = OTP.objects.create(user=user, code=otp_code, expires_at=now() + datetime.timedelta(minutes=5))
    return otp_code

def send_otp_email(user):
    """Sends OTP email to the user."""
    otp_code = generate_otp(user)
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp_code}. It expires in 5 minutes."
    send_mail(subject, message, "your-email@gmail.com", [user.email])

from django.core.mail import send_mail
from django.conf import settings

def send_email_notification(subject, message, recipient_list):
    """Utility function to send an email."""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
