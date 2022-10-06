from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from book.models import Room, Event, Booking
from book.serializers import RoomSerializer, EventSerializer, BookingSerializer


class MultipleFieldLookup():
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_dict = {}
        for field in self.lookup_fields:
            try:
                filter_dict[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter_dict)


class CreateRoomView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RoomSerializer


class DeleteRoomView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'number'


class CreateEventView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventSerializer


class ListEventsAvailableView(generics.ListAPIView):
    queryset = Event.objects.filter(type='public', available=True)
    serializer_class = EventSerializer


class CreateBookingView(generics.CreateAPIView):
    serializer_class = BookingSerializer


class DeleteBookingView(MultipleFieldLookup, generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_fields = ('customer', 'event_name')

    def perform_destroy(self, instance):
        instance.event.available = True
        instance.event.save()
