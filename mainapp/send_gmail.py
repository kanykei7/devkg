from django.core.mail import EmailMessage

from django.conf import settings


def send_msg(email, type_work, company_name):
    mail = EmailMessage(
        f"Hi {company_name}",
        f"Success - {type_work}",
        settings.EMAIL_HOST_USER,
        [email]
    )
    mail.send()
