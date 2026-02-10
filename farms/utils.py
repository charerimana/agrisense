from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sms import send_sms
from .models import Notification
from config import secretKeys

def send_alert(user, reading):
    prefs = user.notification_preference
    message = f"ALERT: Temperature {reading.temperature}°C is out of range."

    if prefs.alerts_enabled:
        if (prefs.email_enabled):
            # message = Mail(
            #     from_email="hareraloston@gmail.com",
            #     to_emails="harerimanacarlos@gmail.com",
            #     subject="Temperature Alert",
            #     html_content=message
            # )
            # sg = SendGridAPIClient(secretKeys.SENDGRID_API_KEY)
            # response = sg.send(message)
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)

            send_mail(
                subject="Temperature Alert",
                message=message,
                from_email="hareraloston@gmail.com",
                recipient_list=[user.email],
                fail_silently=False
            )

        if (prefs.sms_enabled):
            send_sms(
                message,
                "+250780289165",
                [prefs.phone_number],
                fail_silently=False
            )

        Notification.objects.create(
            user=user,
            reading=reading,
            message=message,
            notification_type="EMAIL"
        )
