from django.urls import path
from rent.views import CreateRoomView, CreateEventView, CreateBookingView
from rent.views import ListEventsAvailableView
from rent.views import DeleteRoomView, DeleteBookingView


urlpatterns = [
    path('rooms', CreateRoomView.as_view(), name='create-room'),
    path('rooms/<int:number>', DeleteRoomView.as_view(), name='delete-room'),
    path('events', CreateEventView.as_view(), name='create-event'),
    path('events/available', ListEventsAvailableView.as_view(), name='events-available'),
    path('bookings', CreateBookingView.as_view(), name='create-booking'),
    path('bookings/<str:customer>/<str:event_name>', DeleteBookingView.as_view(),
         name='delete-booking'
         ),
]