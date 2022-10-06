from django.db import models


class Room(models.Model):
    number = models.SmallIntegerField(unique=True, null=False)
    capacity = models.SmallIntegerField(null=False, unique=True)


class Event(models.Model):
    TYPE_CHOICES = [('public', 'public'), ('private', 'private')]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=False)
    name = models.CharField(max_length=100, unique=True, null=False)
    room_number = models.SmallIntegerField(null=False)
    room = models.OneToOneField('Room', on_delete=models.PROTECT, null=False)
    available = models.BooleanField(default=True, null=False)
    date = models.DateField(null=False, unique=True)

    class Meta:
        unique_together = ['room', 'date']


class Booking(models.Model):
    customer = models.CharField(max_length=50, null=False)
    event_name = models.CharField(max_length=100, null=False)
    event = models.ForeignKey('Event', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = ['customer', 'event']