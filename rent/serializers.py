from rest_framework import serializers
from django.utils.translation import gettext as _
from django.db.utils import IntegrityError
from rent.models import Room, Event, Booking

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
            raise serializers.ValidationError(
                _('Cannot book a place: The event is private')
                )

        room = validated_data['event'].room
        date = validated_data['event'].date
        count = Booking.objects.filter(event__room=room, event__date=date).count()
        if count >= room.capacity:
            raise serializers.ValidationError(
                _('Cannot book a place: There is no longer space available for this event')
                )

        try:
            booking = Booking.objects.create(**validated_data)
            if count + 1 >= room.capacity:
                validated_data['event'].available = False
                validated_data['event'].save()
        except IntegrityError as ex:
            raise serializers.ValidationError(
                _('Cannot book a place: You already have a place booked for this event')
                ) from ex
        return booking
