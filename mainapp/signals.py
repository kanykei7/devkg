# from django.db.models.signals import post_save
# from mainapp.models import Vacancy
# from django.dispatch import receiver
# from mainapp.send_gmail import send_msg


# @receiver(post_save, sender=Vacancy)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         send_msg(instance.type_work, instance.salary)