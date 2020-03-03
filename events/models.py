from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save ,post_save
from django.dispatch import receiver
from datetime import datetime


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete = models.CASCADE, related_name='events')
    title = models.CharField(max_length = 100)
    description = models.TextField()
    location =models.CharField(max_length = 180)
    seats = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    logo = models.ImageField(null = True, blank = True)
    booked_seats = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.title

    def remaining_seats(self):
        return self.seats - self.booked_seats

    def is_full(self):
        return self.booked_seats == self.seats

    def can_book(self):
        event_datetime = datetime.combine(self.date, self.time)
        diff = event_datetime - datetime.today()
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        if hours >= 3:
            return True
        return False

@receiver(post_save, sender=Event)
def sendemail_ticket_create(instance, *args, **kwargs):
    if instance:
        followers = Follow.objects.filter(organizer=instance.organizer)
        count = 0
        for follower in followers:
            count += 1
        email = EmailMessage(f"{instance.organizer.username} created an event", f"this email will be sent to {count} users", to=['shaheen.abdelmajeed@outlook.com'])
        email.send()
    else:
        pass


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name='tickets') #which event?
    booker = models.ForeignKey(User, on_delete = models.CASCADE, related_name='tickets') #who is booking?
    number_of_tickets = models.PositiveIntegerField() #how many Tickets for this event?

    def can_cancel(self):
        event_datetime = datetime.combine(self.event.date, self.event.time)
        diff = event_datetime - datetime.today()
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        if hours >= 3:
            return True
        return False

@receiver(pre_save, sender=Ticket)
def sendemail(instance, *args, **kwargs):
    email = EmailMessage('You booked Tickets', f"{instance.booker.username} booked {instance.number_of_tickets} seats for the event ({instance.event.title})", to=['shaheen.abdelmajeed@outlook.com'])
    email.send()

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,related_name='followers')
    organizer = models.ForeignKey(User, on_delete = models.CASCADE)
