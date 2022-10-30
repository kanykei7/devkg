from django.db import models
from django.contrib.auth.models import AbstractUser
from mainapp.conf import *
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):

    def __str__(self) -> str:
        return self.username


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=127)
    description = models.TextField(default='')
    logo = models.ImageField(upload_to='media/company_logo/')
    web_site = models.URLField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=127)
    location = models.CharField(max_length=127)

    def __str__(self):
        return self.name

    @property
    def vacancy_amount(self):
        return self.vacancies.all().count()

    @property
    def event_amount(self):
        return self.events.all().count()

    @property
    def video_amount(self):
        return self.videos.all().count()


class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    type_work = models.CharField(max_length=127)
    type = models.CharField(max_length=127, choices=TYPE)
    salary = models.IntegerField(default=0)
    currency = models.CharField(max_length=127, choices=CURRENCY)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.type_work


class VacancyDescription(models.Model):
    title = models.CharField(max_length=127)
    description = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vacancy_descs')

    def __str__(self):
        return self.title


class Event(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=127)
    description = models.TextField()
    start_at = models.DateTimeField(auto_now=False)
    end_at = models.DateTimeField(auto_now=False)
    location = models.CharField(max_length=127)
    image = models.ImageField(upload_to='events_img')
    price = models.PositiveIntegerField()
    registration = models.URLField(max_length=300)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=127)
    create_at = models.DateField(auto_now_add=True)
    description = models.TextField()
    preview = models.ImageField(upload_to='videos_img')
    video = models.URLField(max_length=300)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Vacancy)
def create_vacancy(sender, instance, created, **kwargs):
    from mainapp.send_gmail import send_msg_vacancy
    if created:
        send_msg_vacancy(instance.type_work, instance.salary, instance.currency)

# @receiver(post_save, sender=Event)
# def create_event(sender, instance, created, **kwargs):
#     from mainapp.send_gmail import send_msg_event
#     if created:
#         send_msg_event(instance.title, instance.description, instance.start_at, instance.end_at, instance.location)
