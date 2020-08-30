# Py-iTrack
A Simple Task Tracker Backend using ReST APIs written in Flask.

## Database-Schema
![iTrack-Schema](./miscellaneous_stuff/iTrackER.jpg)

## Project Structure
```bash
.
├── LICENSE
├── README.md
├── requirements.txt
├── resources
│   ├── development.ini
│   └── production.ini
├── sqlite3.db
└── src
    ├── app.py
    ├── controllers
    │   ├── __init__.py
    │   └── user.py
    ├── main.py
    ├── models
    │   ├── association.py
    │   ├── __init__.py
    │   ├── mixins.py
    │   ├── project.py
    │   ├── static.py
    │   ├── task.py
    │   └── user.py
    ├── routes
    │   ├── __init__.py
    │   └── user.py
    ├── serializers
    │   ├── __init__.py
    │   └── user.py
    └── utils
        ├── __init__.py
        └── misc_instances.py
```
