from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    location =models.CharField(max_length = 180)
    seats = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    logo = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.title
