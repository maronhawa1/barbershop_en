# mailer.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ADMIN_EMAIL = "no-reply@maron-forms.com"   # your verified domain
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


def send_admin_email(name, phone, service, date, hour):
    if not SENDGRID_API_KEY:
        print("Missing SENDGRID_API_KEY, cannot send admin email")
        return

    subject = "New Appointment Requested"
    body = f"""
A new appointment request has been submitted:

Name: {name}
Phone: {phone}
Service: {service}
Date: {date}
Time: {hour}

Please log in to the admin panel to approve or cancel it.
"""

    message = Mail(
        from_email=ADMIN_EMAIL,
        to_emails="maronhawa13@gmail.com",   # your email
        subject=subject,
        plain_text_content=body,
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)


def send_client_email(client_email, name, service, date, hour, status):
    if not SENDGRID_API_KEY:
        print("Missing SENDGRID_API_KEY, cannot send client email")
        return

    if status == "pending":
        subject = "We Received Your Appointment Request - Barber Shop"
        body = f"""
Hello {name},

Your appointment request has been received and is pending approval.

Service: {service}
Date: {date}
Requested Time: {hour}

You will receive another update once it is approved.

Barber Shop 💈
"""
    elif status == "approved":
        subject = "Your Appointment Has Been Approved - Barber Shop"
        body = f"""
Hello {name},

Your appointment has been approved!

Service: {service}
Date: {date}
Time: {hour}

See you soon,
Barber Shop 💈
"""
    elif status == "canceled":
        subject = "Update Regarding Your Appointment - Barber Shop"
        body = f"""
Hello {name},

Unfortunately, your requested appointment was not approved / has been canceled.

Service: {service}
Date: {date}
Time: {hour}

You may book a new appointment through the website.

Barber Shop 💈
"""
    else:
        return

    message = Mail(
        from_email=ADMIN_EMAIL,
        to_emails=client_email,
        subject=subject,
        plain_text_content=body,
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
