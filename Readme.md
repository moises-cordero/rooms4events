# Booking place for an event
###### Django API for technical challenge.
#


### Setup

##### Install dependencies
```sh
$ pip3 install -r requirements.txt
```

##### Create migrations
```sh
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

##### Create superuser
```sh
$ python3 manage.py createsuperuser
```

#

### Run tests
```sh
$ pytest
```

#

### Consume API

| Service | Method | URL | Authorization | Form-data |
| ------ | ------ | ------ | ------ | ------ |
| Create room | POST | localhost:\<port\>/room | Basic Auth (username, password) | number (int), capacity (int) |
| Delete room | DELETE | localhost:\<port\>/room/\<int:number\> | Basic Auth (username, password) |  |
| Create event | POST | localhost:\<port\>/event | Basic Auth (username, password) | type (str), name (str), room_number (int), date (date) |
| Create booking | POST | localhost:\<port\>/booking |  | customer (str), event_name (str) |
| Delete booking | DELETE | localhost:\<port\>/booking/\<str:customer\>/\<str:event_name\> |  |  |
| List available events | GET | localhost:\<port\>/events-available |  |  |
