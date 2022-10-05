from django.urls import path
from rent.views import CreateRoomView, DeleteRoomView, CreateEventView, BookingView
from rent.views import ListPublicEventsView, DeleteBookingView


urlpatterns = [
    path('room', CreateRoomView.as_view(), name='room'),
    path('room/<int:number>', DeleteRoomView.as_view(), name='room'),
    path('event', CreateEventView.as_view(), name='event'),
    path('events', ListPublicEventsView.as_view(), name='events'),
    path('booking', BookingView.as_view(), name='booking'),
    path('booking/<str:customer>/<str:event_name>', DeleteBookingView.as_view(), name='booking'),
]