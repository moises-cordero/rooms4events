from rest_framework import generics
from rent.models import Room, Event, Booking
from rent.serializers import RoomSerializer, EventSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated


class CreateRoomView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoomSerializer


class DeleteRoomView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'number'


class CreateEventView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer


class ListPublicEventsView(generics.ListAPIView):
    queryset = Event.objects.filter(type='public')
    serializer_class = EventSerializer


class BookingView(generics.CreateAPIView):
    serializer_class = BookingSerializer


class DeleteBookingView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'customer'
