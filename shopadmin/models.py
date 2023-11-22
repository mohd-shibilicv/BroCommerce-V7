from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from orders.models import OrderReturn


@receiver(post_save, sender=OrderReturn)
def send_return_approved_email(sender, instance, **kwargs):
    if instance.approved:
        refund_amount = float(instance.order.total_paid) * 0.8
        subject = "Return Request Approved"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]

        email_template = "shopadmin/return_approved_email.html"
        context = {
            "order": instance.order,
            "refund_amount": refund_amount,
        }
        email_message = render_to_string(email_template, context)

        email = EmailMessage(subject, email_message, from_email, recipient_list)
        email.content_subtype = "html"
        email.send()
