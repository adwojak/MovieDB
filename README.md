# MovieDB

**How to use**

* Create virtualenv with python3.8

* Switch to virtualenv and execute command **pip install -r requirements.txt**

* Execute these commands:

  * python manage.py makemigrations moviesapp
  * python manage.py migrate
  * python manage.py runserver

Endpoints:

* **/register/**
  * **POST** - Register. Fields: username, password
  * **PUT** / **PATCH** - Change password. Access token required. Fields: username, password. Id required (/register/<id>/)
* **/delete-user/**
  * **DELETE** - Delete user. Only access token required.
* **/token/**
  * **POST** - Generate JWT token. Fields: username, password
* **/token/refresh/**
  * **POST** - Refresh JWT access token. Refresh token required.
* **/movies/**
  * **GET** - Display movies list. Access token required.
  * **POST** - Add movie from Omdbapi. Access token required. Fields: title
  * **PUT** / **PATCH** - Edit single movie. Access token required. Fields: any from single **GET** entry. Id required (/movies/<id>/)
  * **DELETE** - Delete single movie. Access token required. Id required(/movies/<id>/)
* **/ratings/**
  * **GET** - Display ratings for specific movies. Access token required.
* **/comments/**
  * **GET** - Display list of comments for movies or for specific movie. Access token required. Field movie_id is optional
  * **POST** - Add comment for movie. Access token required. Fields: movie_id, comment
* **/top/**
  * **GET** - Display top comments. Access token required. Optional fields: date_from, date_to
  
