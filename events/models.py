from django.db import models
from django.contrib.auth.models import User


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

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name='tickets') #which event?
    booker = models.ForeignKey(User, on_delete = models.CASCADE, related_name='tickets') #who is booking?
    number_of_tickets = models.PositiveIntegerField() #how many Tickets for this event?
