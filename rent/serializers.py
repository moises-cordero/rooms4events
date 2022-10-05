from rent.models import Room, Event, Booking
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.db.utils import IntegrityError

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'capacity']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['type', 'name', 'room_number', 'date']

    def create(self, validated_data):
        validated_data['room'] = Room.objects.get(number=int(validated_data['room_number']))
        event = Event.objects.create(**validated_data)
        return event


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['customer', 'event_name']

    def create(self, validated_data):
        validated_data['event'] = Event.objects.get(name=validated_data['event_name'])

        if validated_data['event'].type == 'private':
            raise serializers.ValidationError(_('You cannot book a place because the event is private'))

        room = validated_data['event'].room
        if Booking.objects.filter(event__room=room).count() >= room.capacity:
            raise serializers.ValidationError(_('There is no longer space available for this room'))

        try:
            booking = Booking.objects.create(**validated_data)
        except IntegrityError as ex:
            raise serializers.ValidationError(_('You already have a place booked for this event'))
        return booking
