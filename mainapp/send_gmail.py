from django.core.mail import EmailMessage

from django.conf import settings

from mainapp.models import User


# from django.contrib.auth import get_user_model
#
# User = get_user_model()


def send_msg_vacancy(type_work, salary, currency):
    mail = EmailMessage(
        f'Hi, new vacancy "{type_work}"',
        f'Salary - {salary} {currency}',
        settings.EMAIL_HOST_USER,
        User.objects.values_list('email', flat=True)

    )
    mail.send()


# def send_msg_event(title, description, start_at, end_at, location):
#     mail = EmailMessage(
#         f'Hi, new event "{title}"',
#         f'{description}',
#         f'Start at:{start_at} - {end_at}',
#         f'Location: {location}',
#         settings.EMAIL_HOST_USER,
#         User.objects.values_list('email', flat=True)
#
#     )
#     mail.send()
