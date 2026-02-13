from django.core.mail import send_mail
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from config import secretKeys
from sms import send_sms
from .models import Notification
import logging

logger = logging.getLogger(__name__)

def send_alert(user, reading):
    prefs = getattr(user, 'notification_preference', None)

    if not prefs or not prefs.alerts_enabled:
        return 

    message = f"ALERT: Temperature {reading.temperature}°C is out of range for Sensor with ID {reading.sensor.id} at {reading.sensor.farm.name} farm"

    if prefs.email_enabled and user.email:
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

    if prefs.sms_enabled and prefs.phone_number:
        try:
            account_sid = secretKeys.TWILIO_ACCOUNT_SID
            auth_token = secretKeys.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_=secretKeys.TWILIO_PHONE_NUMBER,
                body=message,
                to=prefs.phone_number
            )
        except Exception as e:
            # 'exc_info=True' automatically logs the full Stack Trace (where the error happened)
            logger.error("An unexpected error occurred: %s", e, exc_info=True)


        # send_sms(
        #     message,
        #     "+250780289165",
        #     [prefs.phone_number],
        #     fail_silently=False
        # )

    Notification.objects.create(
        user=user,
        reading=reading,
        message=message,
        notification_type="EMAIL" if prefs.email_enabled else "SMS"
    )
