from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal, receiver
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .token import account_activation_token

user_registered = Signal()


@receiver(user_registered)
def send_activation_email(sender, user, current_site, **kwargs):
    subject = "Activate your account"
    protocol = "https" if isinstance(current_site, HttpRequest) and current_site.is_secure() else "http"
    message = render_to_string(
        "registration/account_activation_token.html",
        {
            "user": user,
            "protocol": protocol,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
