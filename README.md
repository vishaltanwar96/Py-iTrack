# Py-iTrack
A Simple Task Tracker Backend using Flask ReST APIs.

## Database-Schema
![iTrack-Schema](https://i.imgur.com/h4ec8iz.png)

## Project Structure
```bash
.
├── LICENSE
├── README.md
├── requirements.txt
├── resources
│   ├── development.ini
│   └── production.ini
└── src
    ├── app.py
    ├── controllers
    │   └── __init__.py
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
    │   └── __init__.py
    ├── serializers
    │   └── __init__.py
    ├── sqlite3.db
    └── utils
        ├── database.py
        └── __init__.py
```