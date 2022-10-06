import json
import pytest
from django_mock_queries.query import MockSet
from rest_framework.test import force_authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Room, Event, Booking
from book.views import CreateRoomView, CreateEventView, CreateBookingView
from book.views import ListEventsAvailableView
from book.views import DeleteRoomView, DeleteBookingView


@pytest.mark.urls('book.urls')
@pytest.mark.django_db
class Tests:

    def get_user(self):
        return User.objects.create_user(username='temp', email='temp@…', password='temp')

    def test_create_room(self, rf, mocker):
        data = {'number': 100, 'capacity': 100}
        request = rf.post(reverse('create-room'), content_type='application/json',
                          data=json.dumps(data)
                          )
        force_authenticate(request, user=self.get_user())
        mocker.patch.object(Room, 'save')
        response = CreateRoomView.as_view()(request).render()

        assert response.status_code == 201
        assert json.loads(response.content).get('number') == 100 \
            and json.loads(response.content).get('capacity') == 100
        assert Room.save.called

    def test_delete_room(self, rf, mocker):
        request = rf.delete(reverse('delete-room', kwargs={'number': 100}))
        force_authenticate(request, user=self.get_user())
        room = Room(number=100, capacity=100)
        mocker.patch.object(DeleteRoomView, 'get_object', return_value=room)
        mocker.patch.object(Room, 'delete')
        response = DeleteRoomView.as_view()(request).render()

        assert response.status_code == 204
        assert Room.delete.called

    def test_create_event(self, rf, mocker):
        Room.objects.create(number=100, capacity=100)
        data = {'type': 'public', 'name': 'party', 'room_number': 100, 'date': '2023-01-01'}
        request = rf.post(reverse('create-event'), content_type='application/json',
                          data=json.dumps(data)
                          )
        force_authenticate(request, user=self.get_user())
        mocker.patch.object(Event, 'save')
        response = CreateEventView.as_view()(request).render()

        assert response.status_code == 201
        assert json.loads(response.content).get('type') == data['type'] \
            and json.loads(response.content).get('name') == data['name'] \
            and json.loads(response.content).get('room_number') == data['room_number'] \
            and json.loads(response.content).get('date') == data['date']
        assert Event.save.called

    def test_create_booking(self, rf, mocker):
        data = {'customer': 'moises cordero', 'event_name': 'party'}
        room = Room.objects.create(number=100, capacity=100)
        Event.objects.create(type='public', name=data['event_name'], room=room,
                             room_number=room.number, date='2023-01-01'
                             )
        request = rf.post(reverse('create-booking'), content_type='application/json',
                          data=json.dumps(data)
                          )
        force_authenticate(request, user=self.get_user())
        mocker.patch.object(Booking, 'save')
        response = CreateBookingView.as_view()(request).render()

        assert response.status_code == 201
        assert json.loads(response.content).get('customer') == data['customer'] \
            and json.loads(response.content).get('event_name') == data['event_name']
        assert Booking.save.called

    def test_delete_booking(self, rf, mocker):
        data = {'customer': 'moises cordero', 'event_name': 'party'}
        request = rf.delete(reverse('delete-booking', kwargs=data))
        force_authenticate(request, user=self.get_user())
        room = Room.objects.create(number=100, capacity=100)
        event = Event.objects.create(type='public', name=data['event_name'], room=room,
                                     room_number=room.number, date='2023-01-01'
                                     )        
        booking = Booking(customer='moises cordero', event=event, event_name=event.name)
        mocker.patch.object(DeleteBookingView, 'get_object', return_value=booking)
        mocker.patch.object(Booking, 'delete')
        response = DeleteBookingView.as_view()(request).render()

        assert response.status_code == 204
        # assert Booking.delete.called

    def test_list_events_available(self, rf, mocker):
        request = rf.get(reverse('events-available'))
        queryset = MockSet(
            Event(type='public', name='Evento1', room_number=5, date='2022-10-12'),
            Event(type='public', name='Evento1', room_number=5, date='2022-10-12')
        )
        mocker.patch.object(ListEventsAvailableView, 'get_queryset', return_value=queryset)
        response = ListEventsAvailableView.as_view()(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
