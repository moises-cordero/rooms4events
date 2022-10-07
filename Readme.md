# Renting rooms for events
###### Django API to manage a small business that is focused on renting different rooms for events.

## Setup

1. Clone repository
```
git clone https://github.com/moises-cordero/rooms4events.git
cd rooms4events
```

2. Create and activate a virtual environment to install dependencies (optional)
```
python -m venv env
source env/bin/activate
```
 
3. Install dependencies
```
pip install -r requirements.txt
```

4. Create and apply Django migrations
```
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser to the business user (required to consume services with authorization)
```
python manage.py createsuperuser --username <username> --email <email> --noinput
```

6. Start the Django development server to activate the API (the default port is 8000)
```
python manage.py runserver
```

## Run tests
```
pytest
```

## Consume API

To consume the API you can use applications like [Postman](https://www.postman.com/) or [Advanced REST client](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo)

| Service | Method | URL | Authorization | Form-data |
| ------ | ------ | ------ | ------ | ------ |
| Create room | POST | localhost:8000/room | Basic Auth (username, password) | number (int), capacity (int) |
| Delete room | DELETE | localhost:8000/room/\<int:number\> | Basic Auth (username, password) |  |
| Create event | POST | localhost:8000/event | Basic Auth (username, password) | type (str), name (str), room_number (int), date (date) |
| Create booking | POST | localhost:8000/booking |  | customer (str), event_name (str) |
| Delete booking | DELETE | localhost:8000/booking/\<str:customer\>/\<str:event_name\> |  |  |
| List available events | GET | localhost:80000/events/available |  |  |


## Features

- Rules:
  - There are N rooms with M capacity.
  - There are two types of events: public and private.
  - If the event is public, any customer can book a space.
  - If the event is private, no one else can book a space in the room.
  - A customer can book a space for an event, if the event is public and there is still space
available.
  - A customer can cancel its booking and their space should be available again.
  - A customer cannot book a space twice for the same event.

- Requirements:
  - The business can create a room with M capacity.
  - The business can create events for every room.
  - The business can delete a room if said room does not have any events.
  - A customer can book a place for an event.
  - A customer can cancel its booking for an event.
  - A customer can see all the available public events.

- Considerations:
  - For now, there is only one event per day.
  - Each room has a different capacity.
  - Each requirement is an endpoint (a Django view)

## Built With

- Language: Python
- Python Framework: Django
- Rest: Django REST Framework
- Tests: Pytest

## Author
Moisés Cordero

Barranquilla, Colombia

moises.cordero.romero@gmail.com
